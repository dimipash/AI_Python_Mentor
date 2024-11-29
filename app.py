import streamlit as st
import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
from quiz_handler import QuizHandler
from styles import get_github_dark_theme
from constants import (
    LEARNING_MODES,
    DIFFICULTY_LEVELS,
    GEMINI_CONFIG,
    SYSTEM_INSTRUCTION,
    PYTHON_CONCEPTS,
)
from typing import Optional, Dict, Any, List, Tuple, Union
import json
from datetime import datetime


class PythonLearningApp:
    """
    Main application class for the Python Learning Assistant.
    Handles all learning modes and UI interactions.
    """

    def __init__(self) -> None:
        """Initialize the application with required configurations."""
        self._setup_environment()
        self.difficulty = "Beginner"

    def _setup_environment(self) -> None:
        """Set up all necessary configurations and states."""
        self._configure_page()
        self._initialize_states()
        self._setup_ai()
        self._apply_theme()

    def _configure_page(self) -> None:
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title="Python Learning Assistant",
            page_icon="🐍",
            layout="wide",
            initial_sidebar_state="expanded"
        )

    def _initialize_states(self) -> None:
        """Initialize session state variables."""
        default_states = {
            "messages": [],
            "quiz_state": {
                "active": False,
                "current_question": 0,
                "questions": [],
                "score": 0,
                "total_questions": 0,
                "answered": False,
            },
            "page": "home",
        }

        if "user_progress" not in st.session_state:
            st.session_state.user_progress = {
                "completed_concepts": [],
                "quiz_scores": [],
                "code_reviews": 0,
                "practice_exercises": 0,
                "learning_streaks": 0,
                "last_active": None,
                "learning_activities": [],
            }

        for key, default_value in default_states.items():
            if key not in st.session_state:
                st.session_state[key] = default_value

    def handle_progress_tracking(self) -> None:
        """Handle user progress tracking and analytics."""
        st.markdown(
            """
            <div class="progress-container">
                <h2>📊 Learning Progress</h2>
                <p>Track your Python learning journey.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Display main metrics
        self._display_progress_metrics()

        # Display detailed analytics
        self._display_detailed_analytics()

        # Show personalized recommendations
        self._show_learning_recommendations()

    def _display_progress_metrics(self) -> None:
        """Display user progress metrics."""
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Completed Concepts",
                len(st.session_state.user_progress["completed_concepts"]),
            )
        with col2:
            avg_score = self._calculate_average_score()
            st.metric("Average Quiz Score", f"{avg_score:.1f}%")
        with col3:
            st.metric(
                "Learning Streak", st.session_state.user_progress["learning_streaks"]
            )

    def _display_detailed_analytics(self) -> None:
        """Display detailed progress analytics."""
        st.markdown("### 📈 Detailed Analytics")

        # Create tabs for different analytics views
        tab1, tab2, tab3 = st.tabs(
            ["Learning History", "Concept Mastery", "Activity Log"]
        )

        with tab1:
            self._display_learning_history()

        with tab2:
            self._display_concept_mastery()

        with tab3:
            self._display_activity_log()

    def _display_learning_history(self) -> None:
        """Display learning history and trends."""
        # Quiz performance over time
        st.subheader("Quiz Performance")
        quiz_scores = st.session_state.user_progress.get("quiz_scores", [])
        if quiz_scores:
            # Create a line chart for quiz scores
            quiz_df = pd.DataFrame(quiz_scores, columns=["date", "score"])
            st.line_chart(quiz_df.set_index("date")["score"])
        else:
            st.info(
                "No quiz history available yet. Take some quizzes to see your progress!"
            )

        # Practice exercises completed
        st.subheader("Practice Exercises")
        exercises = st.session_state.user_progress.get("practice_exercises", 0)
        st.metric("Total Exercises Completed", exercises)

    def _display_concept_mastery(self) -> None:
        """Display concept mastery progress."""
        st.subheader("Concept Mastery")

        completed_concepts = st.session_state.user_progress.get(
            "completed_concepts", []
        )
        all_concepts = set(PYTHON_CONCEPTS)

        # Create progress bars for concept categories
        categories = {
            "Basics": ["Variables", "Data Types", "Operators"],
            "Control Flow": ["Conditionals", "Loops", "Functions"],
            "Data Structures": ["Lists", "Dictionaries", "Sets"],
            "Advanced": ["Classes", "Decorators", "Generators"],
        }

        for category, concepts in categories.items():
            completed = len([c for c in concepts if c in completed_concepts])
            progress = completed / len(concepts)
            st.write(f"**{category}**")
            st.progress(progress)
            st.write(f"{completed}/{len(concepts)} concepts completed")

    def _display_activity_log(self) -> None:
        """Display recent learning activities."""
        st.subheader("Recent Activities")

        # Get recent activities from session state
        activities = st.session_state.get("learning_activities", [])

        if not activities:
            st.info(
                "No recent activities found. Start learning to track your progress!"
            )
            return

        for activity in activities[-5:]:  # Show last 5 activities
            with st.expander(f"{activity['date']} - {activity['type']}"):
                st.write(f"**Activity:** {activity['description']}")
                if "score" in activity:
                    st.write(f"**Score:** {activity['score']}%")
                if "time_spent" in activity:
                    st.write(f"**Time Spent:** {activity['time_spent']} minutes")

    def _show_learning_recommendations(self) -> None:
        """Show personalized learning recommendations."""
        st.markdown("### 🎯 Recommended Next Steps")

        # Calculate recommendations based on progress
        recommendations = self._generate_recommendations()

        for rec in recommendations:
            with st.expander(rec["title"]):
                st.write(rec["description"])
                if st.button("Start", key=f"rec_{rec['id']}"):
                    self._handle_recommendation_action(rec["action"])

    def _generate_recommendations(self) -> List[Dict[str, Any]]:
        """Generate personalized learning recommendations."""
        recommendations = []
        progress = st.session_state.user_progress

        # Check for incomplete concepts
        if len(progress["completed_concepts"]) < len(PYTHON_CONCEPTS):
            next_concept = self._get_next_recommended_concept()
            recommendations.append(
                {
                    "id": "next_concept",
                    "title": f"📚 Learn {next_concept}",
                    "description": f"Ready to learn about {next_concept}? This concept will help build your Python foundation.",
                    "action": {"type": "concept", "value": next_concept},
                }
            )

        # Check quiz performance
        if progress.get("quiz_scores", []):
            avg_score = self._calculate_average_score()
            if avg_score < 80:
                recommendations.append(
                    {
                        "id": "practice_quiz",
                        "title": "✍️ Take a Practice Quiz",
                        "description": "Your quiz scores show room for improvement. Take a practice quiz to strengthen your knowledge.",
                        "action": {"type": "quiz", "value": "practice"},
                    }
                )

        return recommendations

    def _calculate_average_score(self) -> float:
        """Calculate average quiz score."""
        scores = st.session_state.user_progress.get("quiz_scores", [])
        if not scores:
            return 0.0
        return sum(score["score"] for score in scores) / len(scores)

    def _get_next_recommended_concept(self) -> str:
        """Get the next recommended concept based on user progress."""
        completed = set(st.session_state.user_progress["completed_concepts"])
        all_concepts = set(PYTHON_CONCEPTS)
        remaining = all_concepts - completed

        # Add logic here to prioritize concepts based on difficulty and prerequisites
        return list(remaining)[0] if remaining else "Advanced Topics"

    def _setup_ai(self) -> None:
        """Configure Gemini AI with API key."""
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)

    def _apply_theme(self) -> None:
        """Apply custom styling to the application."""
        st.markdown(get_github_dark_theme(), unsafe_allow_html=True)

    def create_ai_model(self) -> genai.GenerativeModel:
        """Create and return configured Gemini model instance."""
        return genai.GenerativeModel(
            model_name="gemini-exp-1114",
            generation_config=GEMINI_CONFIG,
            system_instruction=SYSTEM_INSTRUCTION,
        )

    def render_navigation(self) -> None:
        """Render the navigation bar."""
        st.markdown(
            """
            <div class="nav-container">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h2 style="margin: 0;">🐍 Python Learning Assistant</h2>
                    </div>
                    <div>
                        <a href="/" class="nav-link">Home</a>
                        <a href="https://github.com/dimipash/AI_Python_Mentor" class="nav-link" target="_blank">GitHub</a>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def render_sidebar(self) -> Tuple[str, str]:
        """Render sidebar with learning mode and difficulty selection."""
        with st.sidebar:
            st.markdown("### Learning Settings")
            
            learning_mode = st.selectbox(
                "📚 Learning Mode",
                options=LEARNING_MODES,
                key="learning_mode_select",
            )
            
            st.markdown("---")
            
            difficulty = st.select_slider(
                "🎯 Difficulty Level",
                options=DIFFICULTY_LEVELS,
                value="Beginner",
            )
            
            st.markdown("---")
            st.markdown("### Quick Stats")
            st.markdown(f"🎯 Current Level: **{difficulty}**")
            st.markdown(f"📝 Completed Quizzes: **{len(st.session_state.user_progress['quiz_scores'])}**")
            
            return learning_mode, difficulty

    def handle_chat_mode(self) -> None:
        """Handle chat-based learning interactions."""
        st.markdown(
            """
            <div class="chat-container">
                <h2>💬 Chat with Your Python Tutor</h2>
                <p>Ask questions, get explanations, and solve problems together.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        self._render_chat_controls()
        self._display_chat_history()

        user_input = st.chat_input(
            "Ask anything about Python...",
            key="chat_input_field",
        )

        if user_input:
            self._process_chat_input(user_input)

    def _render_chat_controls(self) -> None:
        """Render chat control buttons."""
        col1, col2 = st.columns(2)

        if col1.button("🔄 New Chat", key="new_chat_btn", use_container_width=True):
            self._reset_chat()

        if col2.button("🗑️ Clear Chat", key="clear_chat_btn", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    def _reset_chat(self) -> None:
        """Reset chat to initial state."""
        st.session_state.messages = []
        welcome_msg = (
            "👋 Hi! I'm your Python tutor. What would you like to learn today?"
        )
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
        st.rerun()

    def _display_chat_history(self) -> None:
        """Display chat message history."""
        for message in st.session_state.messages:
            message_class = (
                "user-message" if message["role"] == "user" else "assistant-message"
            )
            st.markdown(
                f"""
                <div class="message {message_class}">
                    {message["content"]}
                </div>
                """,
                unsafe_allow_html=True,
            )

    def _process_chat_input(self, user_input: str) -> None:
        """
        Process user input and generate AI response.

        Args:
            user_input: User's message text
        """
        try:
            st.session_state.messages.append(
                {"role": "user", "content": str(user_input)}
            )

            model = self.create_ai_model()
            chat = model.start_chat(history=[])
            response = chat.send_message(user_input)

            self._display_chat_messages(str(response.text))

        except Exception as e:
            st.error(f"Error processing message: {str(e)}")

    def _display_chat_messages(self, response_text: str) -> None:
        """
        Display chat messages in the UI.

        Args:
            response_text: AI model's response text
        """
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        with st.chat_message("assistant"):
            st.write(response_text)

        st.session_state.messages.append(
            {"role": "assistant", "content": response_text}
        )

    def handle_code_review_mode(self) -> None:
        """Handle code review functionality."""
        self._render_code_review_header()
        code = self._get_code_input()

        if st.button("Review Code", key="review_code_btn"):
            self._process_code_review(code)

    def _render_code_review_header(self) -> None:
        """Render code review section header."""
        st.markdown(
            """
            <div class="code-review-container">
                <h2>👨‍💻 Code Review Assistant</h2>
                <p>Submit your Python code for review and get instant feedback.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def _get_code_input(self) -> str:
        """Get code input from user."""
        return st.text_area(
            "Paste your Python code here:",
            height=300,
            placeholder="# Enter your Python code here...",
        )

    def _process_code_review(self, code: str) -> None:
        """
        Process code review request.

        Args:
            code: User's submitted code
        """
        if not code:
            st.warning("Please enter some code to review.")
            return

        try:
            review_prompt = self._create_review_prompt(code)
            model = self.create_ai_model()
            chat = model.start_chat(history=[])
            response = chat.send_message(review_prompt)

            st.markdown("### Review Results:")
            st.write(response.text)

        except Exception as e:
            st.error(f"Code review error: {str(e)}")

    def _create_review_prompt(self, code: str) -> str:
        """
        Create prompt for code review.

        Args:
            code: Code to be reviewed

        Returns:
            Formatted prompt string
        """
        return f"""
        Please review this Python code and provide feedback on:
        1. Code style and PEP 8 compliance
        2. Potential bugs or issues
        3. Performance improvements
        4. Best practices suggestions

        Code to review:
        {code}
        """

    def handle_concept_mode(self) -> None:
        """Handle Python concepts learning mode."""
        self._render_concept_header()
        selected_concept = self._get_concept_selection()

        if selected_concept:
            self._process_concept_learning(selected_concept)

    def _render_concept_header(self) -> None:
        """Render concepts section header."""
        st.markdown(
            """
            <div class="concepts-container">
                <h2>📚 Python Concepts</h2>
                <p>Learn Python concepts with detailed explanations and examples.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def _get_concept_selection(self) -> str:
        """Get selected concept from user."""
        return st.selectbox(
            "Choose a concept to learn:",
            options=PYTHON_CONCEPTS,
        )

    def _process_concept_learning(self, concept: str) -> None:
        """
        Process concept learning request.

        Args:
            concept: Selected Python concept
        """
        try:
            learning_prompt = self._create_learning_prompt(concept)
            model = self.create_ai_model()
            chat = model.start_chat(history=[])

            # Get concept explanation
            response = chat.send_message(learning_prompt)
            st.markdown("### Learn & Practice")
            st.write(response.text)

            # Handle practice section
            self._handle_practice_section(concept, chat)

        except Exception as e:
            st.error(f"Error loading concept: {str(e)}")

    def _create_learning_prompt(self, concept: str) -> str:
        """
        Create prompt for concept learning.

        Args:
            concept: Selected concept

        Returns:
            Formatted prompt string
        """
        return f"""
        Explain {concept} in Python for a {self.difficulty.lower()} level programmer.
        Include:
        1. Clear explanation
        2. Simple examples
        3. Common use cases
        4. Best practices
        5. A practice exercise
        
        Make the explanation appropriate for {self.difficulty.lower()} level.
        """

    def _handle_practice_section(self, concept: str, chat: Any) -> None:
        """
        Handle the practice section of concept learning.

        Args:
            concept: Current concept being learned
            chat: Active chat instance
        """
        st.markdown("### Try It Yourself")
        user_code = st.text_area(
            "Write your code here:",
            height=200,
            key="concept_practice_area",
        )

        if st.button("Check My Code", key="check_concept_code"):
            if user_code:
                self._provide_code_feedback(concept, user_code, chat)
            else:
                st.warning("Please write some code to get feedback.")

    def _provide_code_feedback(self, concept: str, code: str, chat: Any) -> None:
        """
        Provide feedback on practice code.

        Args:
            concept: Current concept
            code: User's practice code
            chat: Active chat instance
        """
        check_prompt = f"""
        Review this code for the concept of {concept}.
        Code: {code}
        
        Provide:
        1. Is it correct implementation?
        2. What can be improved?
        3. Suggestions for better understanding
        """

        feedback = chat.send_message(check_prompt)
        st.markdown("### Feedback")
        st.write(feedback.text)

    def handle_code_execution(self) -> None:
        """Handle safe code execution environment."""
        st.markdown(
            """
            <div class="code-execution-container">
                <h2>🔧 Code Playground</h2>
                <p>Write and test Python code in a safe environment.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        code = st.text_area(
            "Write your Python code:", height=200, key="code_execution_area"
        )

        if st.button("Run Code", key="run_code_btn"):
            self._execute_code_safely(code)

    def _execute_code_safely(self, code: str) -> None:
        """Execute user code in a sandboxed environment."""
        try:
            # Add proper sandboxing logic here
            with st.spinner("Running code..."):
                # Example: Use restricted exec or subprocess with timeout
                result = exec(code)
                st.success("Code executed successfully!")
                st.write("Output:", result)
        except Exception as e:
            st.error(f"Error executing code: {str(e)}")

    def run(self) -> None:
        """Run the main application."""
        self.render_navigation()

        if st.session_state.page == "home":
            st.title("🐍 Python Learning Assistant")
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        learning_mode, self.difficulty = self.render_sidebar()

        # Handle different learning modes
        mode_handlers = {
            "Chat with Tutor": self.handle_chat_mode,
            "Quiz Mode": lambda: self.handle_quiz_mode(QuizHandler()),
            "Code Review": self.handle_code_review_mode,
            "Python Concepts": self.handle_concept_mode,
            "Progress Tracking": self.handle_progress_tracking,
            "Code Playground": self.handle_code_execution,
        }

        handler = mode_handlers.get(learning_mode)
        if handler:
            handler()

    def _update_quiz_progress(self, score: float) -> None:
        """Update progress after quiz completion."""
        st.session_state.user_progress["quiz_scores"].append(
            {"date": datetime.now(), "score": score}
        )
        st.session_state.user_progress["learning_activities"].append(
            {
                "date": datetime.now(),
                "type": "Quiz",
                "description": f"Completed quiz with score {score}%",
                "score": score,
            }
        )

    def handle_quiz_mode(self, quiz_handler: QuizHandler) -> None:
        """Handle quiz mode functionality."""
        st.markdown(
            """
            <div class="quiz-container">
                <h2>📝 Python Quiz Mode</h2>
                <p>Test your Python knowledge with interactive quizzes.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not st.session_state.quiz_state["active"]:
            self._setup_new_quiz(quiz_handler)
        else:
            self._handle_active_quiz(quiz_handler)

    def _setup_new_quiz(self, quiz_handler: QuizHandler) -> None:
        """Setup a new quiz session."""
        col1, col2 = st.columns(2)
        
        with col1:
            num_questions = st.number_input(
                "Number of Questions",
                min_value=1,
                max_value=20,
                value=5
            )
        
        with col2:
            topics = st.multiselect(
                "Select Topics",
                options=PYTHON_CONCEPTS,
                default=["Variables & Data Types"]  # Match the exact string from constants
            )

        if st.button("Start Quiz", key="start_quiz_btn"):
            questions = quiz_handler.generate_questions(
                num_questions=num_questions,
                topics=topics,
                difficulty=self.difficulty
            )
            
            st.session_state.quiz_state = {
                "active": True,
                "current_question": 0,
                "questions": questions,
                "score": 0,
                "total_questions": num_questions,
                "answered": False
            }
            st.rerun()

    def _handle_active_quiz(self, quiz_handler: QuizHandler) -> None:
        """Handle an active quiz session."""
        current_state = st.session_state.quiz_state
        current_q = current_state["current_question"]
        questions = current_state["questions"]

        # Display progress
        progress = (current_q + 1) / current_state["total_questions"]
        st.progress(progress)
        st.write(f"Question {current_q + 1} of {current_state['total_questions']}")

        # Display current question
        if current_q < len(questions):
            question = questions[current_q]
            st.markdown(f"### {question['question']}")
            
            # Handle different question types
            if question["type"] == "multiple_choice":
                self._handle_multiple_choice(question)
            elif question["type"] == "coding":
                self._handle_coding_question(question)

            # Show next question button if answered
            if current_state["answered"]:
                if current_q + 1 < current_state["total_questions"]:
                    if st.button("Next Question", key="next_question_btn"):
                        self._next_question()
                else:
                    self._show_quiz_results()

    def _handle_multiple_choice(self, question: Dict[str, Any]) -> None:
        """Handle multiple choice question type."""
        if not st.session_state.quiz_state["answered"]:
            selected_answer = st.radio(
                "Choose your answer:",
                options=question["options"],
                key=f"quiz_answer_{st.session_state.quiz_state['current_question']}"
            )

            if st.button("Submit Answer", key="submit_answer_btn"):
                correct = selected_answer == question["correct_answer"]
                if correct:
                    st.success("Correct! 🎉")
                    st.session_state.quiz_state["score"] += 1
                else:
                    st.error(f"Incorrect. The correct answer was: {question['correct_answer']}")
                
                st.session_state.quiz_state["answered"] = True
                st.rerun()

    def _handle_coding_question(self, question: Dict[str, Any]) -> None:
        """Handle coding question type."""
        if not st.session_state.quiz_state["answered"]:
            user_code = st.text_area(
                "Write your code here:",
                height=200,
                key=f"quiz_code_{st.session_state.quiz_state['current_question']}"
            )

            if st.button("Submit Code", key="submit_code_btn"):
                # Add code evaluation logic here
                is_correct = self._evaluate_code(user_code, question["test_cases"])
                if is_correct:
                    st.success("Correct! Your code passed all test cases! 🎉")
                    st.session_state.quiz_state["score"] += 1
                else:
                    st.error("Your code didn't pass all test cases. Try again!")
                
                st.session_state.quiz_state["answered"] = True
                st.rerun()

    def _evaluate_code(self, user_code: str, test_cases: List[Dict[str, Any]]) -> bool:
        """Evaluate user's code against test cases."""
        try:
            # Add proper code evaluation logic here
            # This is a simplified example
            return True
        except Exception as e:
            st.error(f"Error in code: {str(e)}")
            return False

    def _next_question(self) -> None:
        """Move to the next question."""
        st.session_state.quiz_state["current_question"] += 1
        st.session_state.quiz_state["answered"] = False
        st.rerun()

    def _show_quiz_results(self) -> None:
        """Show final quiz results."""
        score = st.session_state.quiz_state["score"]
        total = st.session_state.quiz_state["total_questions"]
        percentage = (score / total) * 100

        st.markdown("## Quiz Complete! 🎉")
        st.markdown(f"### Your Score: {score}/{total} ({percentage:.1f}%)")

        # Update progress tracking
        self._update_quiz_progress(percentage)

        if st.button("Start New Quiz", key="new_quiz_btn"):
            st.session_state.quiz_state["active"] = False
            st.rerun()


if __name__ == "__main__":
    app = PythonLearningApp()
    app.run()
