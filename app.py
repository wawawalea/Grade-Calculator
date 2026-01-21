from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from category import Category
from course import Course
import json

app = Flask(__name__)
app.secret_key = 'grade-calculator-secret-key-change-in-production'  # Change this in production

# Predefined course configurations
COURSE_CONFIGS = {
    "Analysis": {
        "categories": [
            {"name": "Homework", "max_score": 40, "item_count": 10},
            {"name": "Midterm", "max_score": 25, "item_count": 1},
            {"name": "Final", "max_score": 35, "item_count": 1}
        ],
        "total_score": 100
    },
    "Parallel Computing": {
        "categories": [
            {"name": "Homework", "max_score": 15, "item_count": 10},
            {"name": "Labs", "max_score": 30, "item_count": 6},
            {"name": "Midterm Exam", "max_score": 25, "item_count": 1},
            {"name": "Final Exam", "max_score": 30, "item_count": 1}
        ],
        "total_score": 100
    },
    "Theory of Computation": {
        "categories": [
            {"name": "Homework", "max_score": 25, "item_count": 8},
            {"name": "Online Quizzes", "max_score": 5, "item_count": 5},
            {"name": "Midterm", "max_score": 30, "item_count": 1},
            {"name": "Final Exam", "max_score": 40, "item_count": 1}
        ],
        "total_score": 100
    }
}

def get_all_courses():
    """Get all courses including predefined and custom ones"""
    all_courses = {}
    all_courses.update(COURSE_CONFIGS)
    
    # Add custom courses from session
    if 'custom_courses' in session:
        all_courses.update(session['custom_courses'])
    
    return all_courses

@app.route('/')
def index():
    """Home page showing available courses"""
    all_courses = get_all_courses()
    custom_courses = session.get('custom_courses', {})
    return render_template('index.html', 
                         courses=all_courses.keys(),
                         predefined_courses=list(COURSE_CONFIGS.keys()),
                         custom_courses=list(custom_courses.keys()))

@app.route('/create-course', methods=['GET', 'POST'])
def create_course():
    """Create or edit a custom course"""
    if request.method == 'GET':
        course_name = request.args.get('edit')
        course_config = None
        if course_name and 'custom_courses' in session and course_name in session['custom_courses']:
            course_config = session['custom_courses'][course_name]
        
        return render_template('create_course.html', course_name=course_name, course_config=course_config)
    
    # POST - save course
    data = request.json
    course_name = data.get('course_name')
    categories_data = data.get('categories', [])
    total_score = float(data.get('total_score', 100))
    
    if not course_name:
        return jsonify({"error": "Course name is required"}), 400
    
    # Initialize custom_courses in session if needed
    if 'custom_courses' not in session:
        session['custom_courses'] = {}
    
    # Validate categories
    categories = []
    for cat_data in categories_data:
        if not cat_data.get('name') or not cat_data.get('item_count') or not cat_data.get('max_score'):
            continue
        categories.append({
            'name': cat_data['name'],
            'item_count': int(cat_data['item_count']),
            'max_score': float(cat_data['max_score'])
        })
    
    if not categories:
        return jsonify({"error": "At least one category is required"}), 400
    
    # Save course
    session['custom_courses'][course_name] = {
        'categories': categories,
        'total_score': total_score
    }
    session.modified = True
    
    return jsonify({"success": True, "redirect": url_for('course_form', course_name=course_name)})

@app.route('/delete-course/<course_name>', methods=['POST'])
def delete_course(course_name):
    """Delete a custom course"""
    if 'custom_courses' in session and course_name in session['custom_courses']:
        del session['custom_courses'][course_name]
        session.modified = True
        return jsonify({"success": True})
    return jsonify({"error": "Course not found"}), 404

@app.route('/course/<course_name>')
def course_form(course_name):
    """Display form for inputting grades for a specific course"""
    all_courses = get_all_courses()
    if course_name not in all_courses:
        return "Course not found", 404
    config = all_courses[course_name]
    is_custom = course_name in session.get('custom_courses', {})
    return render_template('course_form.html', course_name=course_name, config=config, is_custom=is_custom)

@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate and display grades"""
    data = request.json
    course_name = data.get('course_name')
    
    all_courses = get_all_courses()
    if course_name not in all_courses:
        return jsonify({"error": "Course not found"}), 404
    
    config = all_courses[course_name]
    categories = []
    
    # Build categories from form data
    for cat_config in config['categories']:
        cat_name = cat_config['name']
        scores = []
        
        # Get scores for this category
        for i in range(cat_config['item_count']):
            key = f"{cat_name}_{i}"
            score = data.get(key, 0)
            try:
                scores.append(float(score) if score else 0)
            except (ValueError, TypeError):
                scores.append(0)
        
        category = Category(cat_name, scores, cat_config['max_score'])
        categories.append(category)
    
    # Create course and calculate results
    course = Course(course_name, categories, config['total_score'])
    
    # Prepare results data
    results = {
        "course_name": course_name,
        "categories": [],
        "total_achieved": course.total_achieved_score(),
        "total_max": config['total_score'],
        "total_percentage": (course.total_achieved_score() / config['total_score']) * 100
    }
    
    for category in categories:
        results["categories"].append({
            "name": category.name,
            "achieved": category.achieved_score(),
            "max_score": category.max_score,
            "percentage": category.percentage()
        })
    
    return render_template('results.html', results=results, current_scores=data, config=config)

@app.route('/goal', methods=['POST'])
def calculate_goal():
    """Calculate goal scores to reach target grade"""
    data = request.json
    course_name = data.get('course_name')
    target_grade = float(data.get('target_grade', 0))
    
    all_courses = get_all_courses()
    if course_name not in all_courses:
        return jsonify({"error": "Course not found"}), 404
    
    config = all_courses[course_name]
    categories = []
    current_scores_by_item = {}
    
    # Build categories from form data and track individual item scores
    for cat_config in config['categories']:
        cat_name = cat_config['name']
        scores = []
        
        for i in range(cat_config['item_count']):
            key = f"{cat_name}_{i}"
            score = data.get(key, 0)
            try:
                score_val = float(score) if score else 0
                scores.append(score_val)
                current_scores_by_item[key] = score
            except (ValueError, TypeError):
                scores.append(0)
                current_scores_by_item[key] = 0
        
        category = Category(cat_name, scores, cat_config['max_score'])
        categories.append(category)
    
    course = Course(course_name, categories, config['total_score'])
    goal_scores = course.calculate_goal_scores(target_grade, current_scores_by_item, config)
    
    current_total = course.total_achieved_score()
    
    return render_template('goal_results.html', 
                         course_name=course_name,
                         target_grade=target_grade,
                         current_total=current_total,
                         goal_scores=goal_scores,
                         config=config,
                         current_scores=current_scores_by_item)

@app.route('/whatif', methods=['POST'])
def calculate_whatif():
    """Calculate what-if scenario with hypothetical scores"""
    data = request.json
    course_name = data.get('course_name')
    
    all_courses = get_all_courses()
    if course_name not in all_courses:
        return jsonify({"error": "Course not found"}), 404
    
    config = all_courses[course_name]
    categories = []
    current_scores_by_item = {}
    hypothetical_scores = {}
    
    # Build current categories and track scores
    for cat_config in config['categories']:
        cat_name = cat_config['name']
        scores = []
        
        for i in range(cat_config['item_count']):
            key = f"{cat_name}_{i}"
            score = data.get(f"current_{key}", data.get(key, 0))
            try:
                score_val = float(score) if score else 0
                scores.append(score_val)
                current_scores_by_item[key] = score
            except (ValueError, TypeError):
                scores.append(0)
                current_scores_by_item[key] = 0
            
            # Check for hypothetical score
            hyp_key = f"hypothetical_{key}"
            if hyp_key in data:
                try:
                    hyp_val = float(data[hyp_key]) if data[hyp_key] else None
                    if hyp_val is not None:
                        hypothetical_scores[key] = hyp_val
                except (ValueError, TypeError):
                    pass
        
        category = Category(cat_name, scores, cat_config['max_score'])
        categories.append(category)
    
    course = Course(course_name, categories, config['total_score'])
    whatif_results = course.calculate_whatif(hypothetical_scores, current_scores_by_item, config)
    
    return render_template('whatif_results.html', results=whatif_results, hypothetical_scores=hypothetical_scores)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
