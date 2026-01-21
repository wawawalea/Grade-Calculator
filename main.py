from course import Course
from category import Category

# Create Analysis course
# HW: 10 items, max_score = 40 (total possible points for all HWs)
# Midterm: 1 item, max_score = 25
# Final: 1 item, max_score = 35

# Example input scores
hw_scores = [4, 4, 3.5, 4, 3.8, 4, 3.5, 4, 3.9, 3.8]  # 10 homework scores
midterm_score = [22]  # 1 midterm score
final_score = [30]  # 1 final score

# Create categories
hw_category = Category("Homework", hw_scores, max_score=40)
midterm_category = Category("Midterm", midterm_score, max_score=25)
final_category = Category("Final", final_score, max_score=35)

# Create course
Analysis = Course("Analysis", [hw_category, midterm_category, final_category], total_score=100)

# Display results
Analysis.display_results()

# ============================================================================
# Parallel Computing course
# Homework: 15%, Labs: 30%, Midterm: 25%, Final: 30%
# ============================================================================

# Example input scores for Parallel Computing
pc_hw_scores = [1.4, 1.5, 1.3, 1.5, 1.4, 1.4, 1.3, 1.5, 1.4, 1.3]  # 10 homework scores
pc_lab_scores = [5, 5, 4.8, 5, 4.9, 5]  # 6 lab scores
pc_midterm_score = [23]  # 1 midterm score
pc_final_score = [27]  # 1 final score

# Create categories for Parallel Computing
pc_hw_category = Category("Homework", pc_hw_scores, max_score=15)
pc_labs_category = Category("Labs", pc_lab_scores, max_score=30)
pc_midterm_category = Category("Midterm Exam", pc_midterm_score, max_score=25)
pc_final_category = Category("Final Exam", pc_final_score, max_score=30)

# Create course
ParallelComputing = Course("Parallel Computing", 
                           [pc_hw_category, pc_labs_category, pc_midterm_category, pc_final_category], 
                           total_score=100)

# Display results
ParallelComputing.display_results()

# ============================================================================
# Theory of Computation course
# Homework: 25%, Online Quizzes: 5%, Midterm: 30%, Final Exam: 40%
# ============================================================================

# Example input scores for Theory of Computation
toc_hw_scores = [3.2, 3.1, 3.0, 3.2, 2.9, 3.1, 3.0, 3.2]  # 8 homework scores
toc_quiz_scores = [1.0, 0.9, 1.0, 0.95, 0.95]  # 5 online quiz scores
toc_midterm_score = [28]  # 1 midterm score
toc_final_score = [36]  # 1 final score

# Create categories for Theory of Computation
toc_hw_category = Category("Homework", toc_hw_scores, max_score=25)
toc_quizzes_category = Category("Online Quizzes", toc_quiz_scores, max_score=5)
toc_midterm_category = Category("Midterm", toc_midterm_score, max_score=30)
toc_final_category = Category("Final Exam", toc_final_score, max_score=40)

# Create course
TheoryOfComputation = Course("Theory of Computation", 
                             [toc_hw_category, toc_quizzes_category, toc_midterm_category, toc_final_category], 
                             total_score=100)

# Display results
TheoryOfComputation.display_results()