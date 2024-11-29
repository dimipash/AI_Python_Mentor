from typing import List, Dict, Any
import random
from quiz_data import QUIZ_DATA

class QuizHandler:
    """Handles quiz generation and scoring for the Python learning app."""
    
    def __init__(self) -> None:
        self.score = 0
        self.total_questions = 0

    def get_topics(self, difficulty: str) -> List[str]:
        """Get available topics for the given difficulty level."""
        return list(QUIZ_DATA.get(difficulty, {}).keys())

    def generate_questions(
        self, 
        num_questions: int, 
        topics: List[str], 
        difficulty: str
    ) -> List[Dict[str, Any]]:
        """Generate quiz questions based on selected parameters."""
        questions = []
        available_questions = []

        # Collect questions for all selected topics
        for topic in topics:
            topic_questions = QUIZ_DATA.get(difficulty, {}).get(topic, [])
            available_questions.extend(topic_questions)

        if not available_questions:
            return []

        # Select random questions
        num_questions = min(num_questions, len(available_questions))
        selected_questions = random.sample(available_questions, num_questions)

        # Format questions for UI
        for question in selected_questions:
            questions.append({
                "type": "multiple_choice",
                "question": question["question"],
                "options": question["options"],
                "correct_answer": question["options"][question["correct"]],
                "explanation": question["explanation"]
            })

        return questions

    def check_answer(self, question: Dict[str, Any], selected_option: str) -> Dict[str, Any]:
        """Validate the selected answer and provide feedback."""
        is_correct = selected_option == question["correct_answer"]
        return {
            "is_correct": is_correct,
            "explanation": question["explanation"],
            "correct_answer": question["correct_answer"]
        }

    def calculate_score(self, correct: int, total: int) -> float:
        """Calculate percentage score."""
        return (correct / total * 100) if total > 0 else 0
