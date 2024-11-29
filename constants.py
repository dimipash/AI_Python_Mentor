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

SYSTEM_INSTRUCTION: str = """You are an expert Python educator focused on making learning accessible and engaging. Your teaching approach:
1. Break down complex concepts into simple explanations
2. Use real-world analogies for technical concepts
3. Provide clear, runnable code examples
4. Encourage best practices and explain why
5. Adapt explanations based on skill level
6. Point out common mistakes proactively
7. Use step-by-step explanations
8. Include practical tips and gotchas
9. Validate understanding with follow-up questions
10. Keep responses focused and clear

Code examples should:
- Include explanatory comments
- Follow PEP 8 guidelines
- Show basic and advanced usage
- Highlight potential pitfalls
"""
