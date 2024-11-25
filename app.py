import streamlit as st
import os
from typing import Optional
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


class PythonLearningApp:
    def __init__(self):
        self._setup_page_config()
        self._initialize_session_state()
        self._setup_gemini()
        self._apply_styling()
        self.difficulty = "Beginner"

    def _setup_page_config(self) -> None:
        """Configure initial Streamlit page settings."""
        st.set_page_config(
            page_title="Python Learning Assistant",
            page_icon="🐍",
            layout="wide",
        )

    def _initialize_session_state(self) -> None:
        """Initialize Streamlit session state variables."""
        if "messages" not in st.session_state:
            st.session_state.messages = []

        if "quiz_state" not in st.session_state:
            st.session_state.quiz_state = {
                "active": False,
                "current_question": 0,
                "questions": [],
                "score": 0,
                "total_questions": 0,
                "answered": False,
            }

        if "page" not in st.session_state:
            st.session_state.page = "home"

    def _setup_gemini(self) -> None:
        """Configure Gemini AI with API key."""
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)

    def _apply_styling(self) -> None:
        """Apply custom styling to the app."""
        st.markdown(get_github_dark_theme(), unsafe_allow_html=True)

    def create_gemini_model(self) -> genai.GenerativeModel:
        """Create and configure Gemini model instance."""
        return genai.GenerativeModel(
            model_name="gemini-exp-1114",
            generation_config=GEMINI_CONFIG,
            system_instruction=SYSTEM_INSTRUCTION,
        )

    def render_welcome_screen(self) -> None:
        """Render an engaging welcome screen."""
        st.markdown(
            """
            <div class="animate-fade-in">
                <h1 style='text-align: center; color: #58a6ff;'>🐍 Python Learning Assistant</h1>
                <div style='text-align: center; margin: 2rem 0;'>
                    <p style='font-size: 1.2rem;'>Your personal AI-powered Python tutor</p>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

        # Feature cards
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                """
                <div class="stCard">
                    <h3>📚 Interactive Learning</h3>
                    <p>Learn Python through conversations, exercises, and quizzes</p>
                </div>
            """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
                <div class="stCard">
                    <h3>🎯 Personalized Path</h3>
                    <p>Adaptive content based on your skill level and goals</p>
                </div>
            """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                """
                <div class="stCard">
                    <h3>💻 Hands-on Practice</h3>
                    <p>Real-world examples and immediate feedback</p>
                </div>
            """,
                unsafe_allow_html=True,
            )

    def render_navigation(self) -> None:
        """Render navigation menu."""
        st.markdown(
            """
            <div class="nav-container">
                <a href="/" target="_self" class="nav-link">🏠 Home</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def render_sidebar(self) -> tuple[str, str]:
        """Render an improved sidebar with better UX."""
        with st.sidebar:
            try:
                st.markdown(
                    """
                    <div style='text-align: center; margin-bottom: 1rem;'>
                        <h2>Learning Dashboard</h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Format progress number as string
                progress = "75"  # or calculate actual progress
                st.markdown(
                    f"""
                    <div class="progress-card">
                        <div class="progress-number">{progress}%</div>
                        <p>Learning Progress</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

                learning_mode = st.selectbox(
                    "🎯 Choose Your Learning Mode",
                    options=LEARNING_MODES,
                    key="learning_mode_select",
                )

                difficulty = st.select_slider(
                    "📊 Select Difficulty Level",
                    options=DIFFICULTY_LEVELS,
                    value="Beginner",
                )

                st.markdown(
                    """
                    <div class="tooltip" style='text-align: center; margin-top: 1rem;'>
                        ℹ️ Need help choosing?
                        <span class="tooltiptext">Select based on your Python experience</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                return learning_mode, difficulty

            except Exception as e:
                st.error("⚠️ Error loading sidebar components")
                st.error(f"Details: {str(e)}")
                # Provide fallback values in case of error
                return LEARNING_MODES[0], DIFFICULTY_LEVELS[0]  # Return default values


    def handle_chat_mode(self) -> None:
        """Enhanced chat mode with better UX."""
        st.markdown(
            """
            <div class="chat-container">
                <h2>💬 Chat with Your Python Tutor</h2>
                <p>Ask questions, get explanations, and solve problems together.</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

        # Control buttons with improved styling
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 New Chat", key="new_chat_btn", use_container_width=True):
                st.session_state.messages = []
                welcome_msg = (
                    "👋 Hi! I'm your Python tutor. What would you like to learn today?"
                )
                st.session_state.messages.append(
                    {"role": "assistant", "content": welcome_msg}
                )
                st.rerun()

        with col2:
            if st.button(
                "🗑️ Clear Chat", key="clear_chat_btn", use_container_width=True
            ):
                st.session_state.messages = []
                st.rerun()

        # Chat messages with improved styling
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

        # Chat input with placeholder
        user_input = st.chat_input(
            "Ask anything about Python...",
            key="chat_input_field",
        )

    def display_loading_animation(self) -> None:
        """Display a loading animation."""
        st.markdown(
            """
            <div style='text-align: center;'>
                <div class="loading"></div>
                <p>Processing your request...</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    # Modify _process_chat_input to handle JSON serialization safely
    def _process_chat_input(self, user_input: str) -> None:
        """Process user chat input and generate response."""
        try:
            # Ensure message is JSON-serializable
            st.session_state.messages.append({
                "role": "user",
                "content": str(user_input)  # Ensure content is string
            })

            model = self.create_gemini_model()
            chat = model.start_chat(history=[])
            response = chat.send_message(user_input)

            # Ensure response is properly serialized
            response_text = str(response.text)
            self._display_chat_messages(response_text)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


    def _display_chat_messages(self, response_text: str) -> None:
        """Display chat messages in the UI."""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        with st.chat_message("assistant"):
            st.write(response_text)

        st.session_state.messages.append(
            {"role": "assistant", "content": response_text}
        )

    def run(self) -> None:
        """Run the main application."""
        self.render_navigation()

        if st.session_state.page == "home":
            st.title("🐍 Python Learning Assistant")
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        learning_mode, self.difficulty = self.render_sidebar()

        if learning_mode == "Chat with Tutor":
            self.handle_chat_mode()
        elif learning_mode == "Quiz Mode":
            quiz_handler = QuizHandler()
            self.handle_quiz_mode(quiz_handler)

    def handle_quiz_mode(self, quiz_handler: QuizHandler) -> None:
        """Handle Quiz Mode functionality."""
        if not st.session_state.quiz_state["active"]:
            self._setup_new_quiz(quiz_handler)
        else:
            self._handle_active_quiz(quiz_handler)

    def _setup_new_quiz(self, quiz_handler: QuizHandler) -> None:
        """Setup a new quiz session."""
        try:
            st.info("Test your Python knowledge with our interactive quizzes!")
            topics = quiz_handler.get_quiz_topics(self.difficulty)

            if topics:
                selected_topic = st.selectbox("Select Topic:", topics)
                num_questions = st.slider("Number of Questions:", 1, 10, 5)

                if st.button("Start Quiz", key="start_quiz_btn"):
                    questions = quiz_handler.generate_quiz(
                        self.difficulty, selected_topic, num_questions
                    )
                    # Ensure all data is JSON-serializable
                    st.session_state.quiz_state = {
                        "active": bool(True),
                        "current_question": int(0),
                        "questions": [dict(q) for q in questions],  # Ensure questions are dicts
                        "score": int(0),
                        "total_questions": int(len(questions)),
                        "answered": bool(False),
                    }
                    st.rerun()
        except Exception as e:
            st.error(f"Quiz setup error: {str(e)}")


    def _handle_active_quiz(self, quiz_handler: QuizHandler) -> None:
        """Handle an active quiz session."""
        current_q = st.session_state.quiz_state["current_question"]
        questions = st.session_state.quiz_state["questions"]

        if current_q < len(questions):
            question = questions[current_q]
            st.write(f"Question {current_q + 1} of {len(questions)}:")
            st.write(question["question"])

            option = st.radio(
                "Select your answer:", question["options"], key=f"q_{current_q}"
            )

            selected_index = question["options"].index(option)

            if not st.session_state.quiz_state["answered"]:
                if st.button("Submit Answer", key="submit_answer_btn"):
                    result = quiz_handler.check_answer(question, selected_index)

                    if result["is_correct"]:
                        st.success("Correct! 🎉")
                        st.session_state.quiz_state["score"] += 1
                    else:
                        st.error(
                            f"Incorrect. The correct answer was: {result['correct_answer']}"
                        )

                    st.info(f"Explanation: {result['explanation']}")
                    st.session_state.quiz_state["answered"] = True
                    st.rerun()

            else:
                if st.button("Next Question", key="next_question_btn"):
                    st.session_state.quiz_state["current_question"] += 1
                    st.session_state.quiz_state["answered"] = False
                    st.rerun()

        else:
            final_score = quiz_handler.calculate_score(
                st.session_state.quiz_state["score"],
                st.session_state.quiz_state["total_questions"],
            )

            st.success(f"Quiz Completed! Your Score: {final_score:.1f}%")
            if st.button("Start New Quiz", key="new_quiz_btn"):
                st.session_state.quiz_state["active"] = False
                st.rerun()

    def handle_quiz_mode(self, quiz_handler: QuizHandler) -> None:
        """Handle Quiz Mode functionality."""
        if not st.session_state.quiz_state["active"]:
            self._setup_new_quiz(quiz_handler)
        else:
            self._handle_active_quiz(quiz_handler)


if __name__ == "__main__":
    app = PythonLearningApp()
    app.run()
