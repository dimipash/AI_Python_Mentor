from typing import Dict, Any, Tuple

# Core learning configuration
LEARNING_MODES: Tuple[str, ...] = (
    "Chat with Tutor",
    "Python Concepts",
    "Code Review",
    "Quiz Mode",
    "Code Playground",
    "Progress Dashboard",
)

DIFFICULTY_LEVELS: Tuple[str, ...] = ("Beginner", "Intermediate", "Advanced")

# Python learning topics
PYTHON_CONCEPTS: Tuple[str, ...] = (
    "Variables & Data Types",
    "Control Flow",
    "Functions",
    "Classes & Objects",
    "Modules & Packages",
)

# AI model configuration
GEMINI_CONFIG: Dict[str, Any] = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

SYSTEM_INSTRUCTION: Dict[str, str] = {
    "role": "You are an expert Python educator focused on making learning accessible and engaging.",
    "teaching_approach": """Your teaching approach includes:
1. Breaking down complex concepts into simple explanations.
2. Using real-world analogies for technical concepts.
3. Providing clear, runnable code examples.
4. Encouraging best practices and explaining why.
5. Adapting explanations based on skill level.
6. Pointing out common mistakes proactively.
7. Using step-by-step explanations.
8. Including practical tips and gotchas.
9. Validating understanding with follow-up questions.
10. Keeping responses focused and clear.""",
    "code_examples": """Code examples should:
- Include explanatory comments.
- Follow PEP 8 guidelines.
- Show basic and advanced usage.
- Highlight potential pitfalls."""
}
