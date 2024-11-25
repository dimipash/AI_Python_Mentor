# Sample quiz questions organized by difficulty and topic
QUIZ_DATA = {
    "Beginner": {
        "Variables & Data Types": [
            {
                "question": "What is the output of: x = 5; print(type(x))?",
                "options": [
                    "<class 'int'>",
                    "<class 'str'>",
                    "<class 'float'>",
                    "<class 'bool'>",
                ],
                "correct": 0,
                "explanation": "In Python, whole numbers are of type 'int' by default.",
            },
            {
                "question": "Which is the correct way to create a string in Python?",
                "options": ["'Hello'", "Hello", "@Hello", "Hello$"],
                "correct": 0,
                "explanation": "Strings in Python are created using single or double quotes.",
            },
        ],
        "Control Flow": [
            {
                "question": "What is the output of: if True: print('Python')?",
                "options": ["Python", "True", "False", "Error"],
                "correct": 0,
                "explanation": "When the if condition is True, the code block is executed.",
            }
        ],
    },
    "Intermediate": {
        "Functions": [
            {
                "question": "What is the output of:\ndef func(x, y=10): return x + y\nprint(func(5))?",
                "options": ["15", "5", "10", "Error"],
                "correct": 0,
                "explanation": "When y is not provided, it uses the default value 10.",
            }
        ],
        "Lists": [
            {
                "question": "What is the output of: [1, 2, 3].append([4, 5])?",
                "options": [
                    "[1, 2, 3, [4, 5]]",
                    "[1, 2, 3, 4, 5]",
                    "[1, 2, 3]",
                    "Error",
                ],
                "correct": 0,
                "explanation": "append() adds the entire object as a single element.",
            }
        ],
    },
    "Advanced": {
        "Classes & Objects": [
            {
                "question": "What is the output of:\nclass A:\n    def __init__(self): print('A')\nA()?",
                "options": ["A", "None", "Error", "Object"],
                "correct": 0,
                "explanation": "The constructor prints 'A' when the object is created.",
            }
        ],
        "Generators": [
            {
                "question": "What type of object is returned by a generator function?",
                "options": ["Generator iterator", "List", "Tuple", "Dictionary"],
                "correct": 0,
                "explanation": "Generator functions return generator iterator objects.",
            }
        ],
    },
}
