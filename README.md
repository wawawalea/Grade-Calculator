# Grade Calculator Web Application

A comprehensive web-based grade calculator that helps you calculate your course grades easily. Create custom courses or use predefined templates!

## Features

### Core Functionality
- **Custom Course Creation**: Create your own courses with custom categories, item counts, and max scores
- **Predefined Courses**: Get started quickly with pre-configured courses:
  - Analysis
  - Parallel Computing
  - Theory of Computation
- **Grade Calculation**: Input scores for each category and get detailed breakdowns with percentages
- **Goal Calculator**: Set a target grade and calculate what scores you need on remaining items
- **What-If Calculator**: Simulate different score scenarios to see how they affect your final grade
- **Course Management**: Edit and delete your custom courses

### User Interface
- Modern, responsive web interface
- Easy-to-use forms for creating courses and entering scores
- Beautiful visualizations of grade breakdowns

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python3 app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Select a course, enter your scores, and view your grade breakdown!

## Project Structure

```
Grade Calculator/
├── app.py              # Flask web application
├── category.py         # Category class definition
├── course.py           # Course class definition
├── main.py             # Command-line version (optional)
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html       # Base template
│   ├── index.html      # Home page
│   ├── course_form.html # Grade input form
│   └── results.html    # Results display
└── README.md           # This file
```

## Usage

### Creating a Custom Course

1. Click "Create Custom Course" on the home page
2. Enter your course name and total score (default: 100)
3. Add categories (e.g., Homework, Exams, Labs):
   - Category name
   - Maximum score for the category
   - Number of items in the category
4. Click "Create Course" to save

### Calculating Grades

1. Select a course from the home page (predefined or custom)
2. Enter your scores for each assignment/category
3. Click "Calculate Grades" to see your results
4. View your total score and percentage for each category

### Goal Calculator

1. After calculating grades, click "🎯 Goal Calculator"
2. Enter your target final grade
3. View the minimum scores needed on remaining items to reach your goal
4. Scores are distributed across categories for a balanced approach

### What-If Calculator

1. After calculating grades, click "🔮 What-If Calculator"
2. Enter hypothetical scores for any items
3. Leave fields blank to use current scores
4. See how different scenarios affect your final grade

### Managing Courses

- **Edit**: Click the ✏️ button on any custom course
- **Delete**: Click the 🗑️ button on any custom course (this cannot be undone)

Enjoy calculating your grades! 🎓
