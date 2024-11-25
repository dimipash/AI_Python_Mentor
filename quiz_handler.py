import random
from quiz_data import QUIZ_DATA


class QuizHandler:
    def __init__(self):
        self.current_score = 0
        self.total_questions = 0

    def get_quiz_topics(self, difficulty):
        """Return available topics for the selected difficulty."""
        return list(QUIZ_DATA.get(difficulty, {}).keys())

    def generate_quiz(self, difficulty, topic, num_questions=5):
        """Generate a quiz with specified parameters."""
        available_questions = QUIZ_DATA.get(difficulty, {}).get(topic, [])
        if not available_questions:
            return []

        # Randomly select questions
        num_questions = min(num_questions, len(available_questions))
        return random.sample(available_questions, num_questions)

    def check_answer(self, question, selected_option):
        """Check if the selected answer is correct."""
        correct_index = question["correct"]
        is_correct = selected_option == correct_index
        return {
            "is_correct": is_correct,
            "explanation": question["explanation"],
            "correct_answer": question["options"][correct_index],
        }

    def calculate_score(self, correct_answers, total_questions):
        """Calculate the percentage score."""
        if total_questions == 0:
            return 0
        return (correct_answers / total_questions) * 100
