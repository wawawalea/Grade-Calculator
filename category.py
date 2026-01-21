class Category:
    def __init__(self, name, items, max_score):
        self.name = name
        self.items = items  # array of scores achieved
        self.max_score = max_score  # maximum possible score for this category
        
    def achieved_score(self):
        """Returns the total score achieved in this category"""
        return sum(self.items)
    
    def percentage(self):
        """Returns the percentage achieved in this category (0-100)"""
        if self.max_score == 0:
            return 0
        return (self.achieved_score() / self.max_score) * 100
