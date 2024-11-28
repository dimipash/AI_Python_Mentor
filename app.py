import streamlit as st
import os
from typing import Optional, Dict, Any, List, Tuple
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

        for key, default_value in default_states.items():
            if key not in st.session_state:
                st.session_state[key] = default_value

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
                <a href="/" target="_self" class="nav-link">🏠 Home</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def render_sidebar(self) -> Tuple[str, str]:
        """
        Render sidebar with learning mode and difficulty selection.
        Returns:
            Tuple containing selected learning mode and difficulty level
        """
        with st.sidebar:
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
        welcome_msg = "👋 Hi! I'm your Python tutor. What would you like to learn today?"
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
        st.rerun()

    def _display_chat_history(self) -> None:
        """Display chat message history."""
        for message in st.session_state.messages:
            message_class = "user-message" if message["role"] == "user" else "assistant-message"
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
            st.session_state.messages.append({
                "role": "user",
                "content": str(user_input)
            })

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

        st.session_state.messages.append({
            "role": "assistant",
            "content": response_text
        })

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
        }

        handler = mode_handlers.get(learning_mode)
        if handler:
            handler()


if __name__ == "__main__":
    app = PythonLearningApp()
    app.run()
