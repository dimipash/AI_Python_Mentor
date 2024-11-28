from typing import Tuple, Dict, Any

# Learning mode options
LEARNING_MODES: Tuple[str, ...] = (
    "Chat with Tutor",
    "Python Concepts",
    "Coding Exercises",
    "Code Review",
    "Quiz Mode",
    "Code Playground",
    "Progress Dashboard",
)

PYTHON_CONCEPTS = [
    "Variables and Data Types",
    "Control Flow (if/else)",
    "Loops (for/while)",
    "Functions",
    "Lists and List Comprehensions",
    "Dictionaries",
    "Sets and Tuples",
    "Object-Oriented Programming",
    "Exception Handling",
    "File Handling",
    "Modules and Packages",
    "Lambda Functions",
    "Decorators",
    "Generators",
    "Context Managers",
]

# Difficulty levels
DIFFICULTY_LEVELS: Tuple[str, ...] = ("Beginner", "Intermediate", "Advanced")

# Gemini AI configuration
GEMINI_CONFIG: Dict[str, Any] = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

SYSTEM_INSTRUCTION: str = """You are an expert Python educator focused on making learning accessible and engaging. Your teaching approach:

1. Break down complex concepts into simple, digestible explanations
2. Use real-world analogies to explain technical concepts
3. Provide clear, runnable code examples for every concept
4. Encourage best practices and explain why they matter
5. Adapt explanations based on the student's level (beginner/intermediate/advanced)
6. Point out common mistakes and misconceptions proactively
7. Use a step-by-step approach when explaining solutions
8. Include practical tips and gotchas that developers encounter
9. Validate understanding by asking relevant follow-up questions
10. Keep responses focused and avoid unnecessary technical jargon

When providing code examples:
- Include comments explaining key points
- Follow PEP 8 style guidelines
- Show both basic and slightly more advanced usage
- Highlight potential pitfalls
"""

# Python concepts topics
PYTHON_CONCEPTS: Tuple[str, ...] = (
    "Variables & Data Types",
    "Control Flow",
    "Functions",
    "Classes & Objects",
    "Modules & Packages",
)
