from category import Category
import math

class Course:
    def __init__(self, name, categories, total_score=100):
        self.name = name
        self.categories = categories  # array of Category objects
        self.total_score = total_score  # total possible score for the course
        
    def total_achieved_score(self):
        """Returns the total score achieved across all categories"""
        return sum(category.achieved_score() for category in self.categories)
    
    def display_results(self):
        """Displays the score for each category and the final total score"""
        print(f"\n{self.name} Course Results:")
        print("=" * 40)
        for category in self.categories:
            achieved = category.achieved_score()
            percentage = category.percentage()
            print(f"{category.name}: {achieved:.2f}/{category.max_score} ({percentage:.2f}%)")
        print("-" * 40)
        total_achieved = self.total_achieved_score()
        total_percentage = (total_achieved / self.total_score) * 100
        print(f"Total Score: {total_achieved:.2f}/{self.total_score} ({total_percentage:.2f}%)")
        print("=" * 40)
    
    def calculate_goal_scores(self, target_grade, current_scores_by_item, config):
        """
        Calculate minimum goal scores for remaining items to achieve target grade.
        Favors most distributed approach across categories.
        
        Args:
            target_grade: Target final score (out of total_score)
            current_scores_by_item: Dict with keys like "CategoryName_0", "CategoryName_1", etc.
            config: Course configuration with category info
        
        Returns:
            Dict with goal scores for each item that needs to be improved
        """
        current_total = self.total_achieved_score()
        needed_score = target_grade - current_total
        
        if needed_score <= 0:
            return {}  # Already achieved or exceeded target
        
        # Find remaining items and their potential contribution
        remaining_items = []
        
        for cat_config in config['categories']:
            cat_name = cat_config['name']
            max_per_item = cat_config['max_score'] / cat_config['item_count']
            
            for i in range(cat_config['item_count']):
                key = f"{cat_name}_{i}"
                current_score = float(current_scores_by_item.get(key, 0) or 0)
                
                # Calculate how much more this item can contribute
                remaining_potential = max_per_item - current_score
                
                if remaining_potential > 0:
                    remaining_items.append({
                        'key': key,
                        'category': cat_name,
                        'index': i,
                        'current': current_score,
                        'max_per_item': max_per_item,
                        'remaining_potential': remaining_potential,
                        'item_count': cat_config['item_count']
                    })
        
        if not remaining_items:
            return {}  # No remaining items
        
        # Sort by item_count (favor categories with more items for distribution)
        # Then by remaining potential
        remaining_items.sort(key=lambda x: (-x['item_count'], -x['remaining_potential']))
        
        # Distribute needed score across remaining items
        goal_scores = {}
        total_distributed = 0
        
        # Calculate proportional distribution
        total_potential = sum(item['remaining_potential'] for item in remaining_items)
        
        if total_potential < needed_score:
            # Not enough potential to reach target
            # Distribute all available potential
            for item in remaining_items:
                goal_scores[item['key']] = {
                    'current': item['current'],
                    'goal': item['max_per_item'],
                    'needed': item['remaining_potential']
                }
            return goal_scores
        
        # Distribute proportionally, but favor equal distribution
        # First pass: equal distribution per category
        category_needs = {}
        for item in remaining_items:
            if item['category'] not in category_needs:
                category_needs[item['category']] = []
            category_needs[item['category']].append(item)
        
        # Distribute proportionally within each category
        for category, items in category_needs.items():
            category_potential = sum(item['remaining_potential'] for item in items)
            if category_potential > 0:
                category_share = (category_potential / total_potential) * needed_score
                
                # Distribute within category
                for item in items:
                    item_share = (item['remaining_potential'] / category_potential) * category_share
                    goal_score = min(item['current'] + item_share, item['max_per_item'])
                    needed = max(0, goal_score - item['current'])
                    
                    if needed > 0.01:  # Only include if meaningful difference
                        goal_scores[item['key']] = {
                            'current': item['current'],
                            'goal': goal_score,
                            'needed': needed
                        }
        
        return goal_scores
    
    def calculate_whatif(self, hypothetical_scores, current_scores_by_item, config):
        """
        Calculate what the final grade would be with hypothetical scores.
        
        Args:
            hypothetical_scores: Dict with keys like "CategoryName_0" and hypothetical values
            current_scores_by_item: Dict with all current scores
            config: Course configuration
        
        Returns:
            Dict with what-if results
        """
        # Merge current and hypothetical scores
        merged_scores = current_scores_by_item.copy()
        merged_scores.update(hypothetical_scores)
        
        # Rebuild categories with merged scores
        whatif_categories = []
        for cat_config in config['categories']:
            cat_name = cat_config['name']
            scores = []
            
            for i in range(cat_config['item_count']):
                key = f"{cat_name}_{i}"
                score = merged_scores.get(key, 0)
                try:
                    scores.append(float(score) if score else 0)
                except (ValueError, TypeError):
                    scores.append(0)
            
            category = Category(cat_name, scores, cat_config['max_score'])
            whatif_categories.append(category)
        
        # Create temporary course with what-if scores
        whatif_course = Course(self.name, whatif_categories, self.total_score)
        
        total_achieved = whatif_course.total_achieved_score()
        total_percentage = (total_achieved / self.total_score) * 100
        
        # Compare with current
        current_total = self.total_achieved_score()
        difference = total_achieved - current_total
        
        results = {
            "course_name": self.name,
            "categories": [],
            "total_achieved": total_achieved,
            "total_max": self.total_score,
            "total_percentage": total_percentage,
            "current_total": current_total,
            "difference": difference
        }
        
        for category in whatif_categories:
            results["categories"].append({
                "name": category.name,
                "achieved": category.achieved_score(),
                "max_score": category.max_score,
                "percentage": category.percentage()
            })
        
        return results