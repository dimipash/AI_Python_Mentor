def get_github_dark_theme():
    return """
    <style>
        /* Modern Dark Theme */
        :root {
            --main-bg-color: #0d1117;
            --secondary-bg: #161b22;
            --text-color: #c9d1d9;
            --accent-color: #58a6ff;
            --success-color: #238636;
            --warning-color: #9e6a03;
            --error-color: #da3633;
            --border-color: #30363d;
        }

        /* General styling */
        .stApp {
            background-color: var(--main-bg-color);
            color: var(--text-color);
        }

        /* Navigation */
        .nav-container {
            background-color: var(--secondary-bg);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .nav-link {
            color: var(--accent-color) !important;
            text-decoration: none;
            font-weight: 600;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            transition: all 0.3s ease;
        }

        .nav-link:hover {
            background-color: rgba(88, 166, 255, 0.1);
        }

        /* Cards */
        .stCard {
            background-color: var(--secondary-bg);
            border-radius: 10px;
            padding: 1.5rem;
            border: 1px solid var(--border-color);
            margin: 1rem 0;
            transition: transform 0.2s ease;
        }

        .stCard:hover {
            transform: translateY(-2px);
        }

        /* Buttons */
        .stButton button {
            border-radius: 6px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }

        .primary-btn {
            background-color: var(--accent-color) !important;
            color: white !important;
        }

        .success-btn {
            background-color: var(--success-color) !important;
            color: white !important;
        }

        /* Chat container */
        .chat-container {
            background-color: var(--secondary-bg);
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            border: 1px solid var(--border-color);
        }

        .message {
            padding: 0.8rem;
            margin: 0.5rem 0;
            border-radius: 8px;
        }

        .user-message {
            background-color: rgba(88, 166, 255, 0.1);
            margin-left: 2rem;
        }

        .assistant-message {
            background-color: rgba(35, 134, 54, 0.1);
            margin-right: 2rem;
        }

        /* Progress indicators */
        .progress-card {
            background-color: var(--secondary-bg);
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            border: 1px solid var(--border-color);
        }

        .progress-number {
            font-size: 2rem;
            font-weight: bold;
            color: var(--accent-color);
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .animate-fade-in {
            animation: fadeIn 0.5s ease-in;
        }

        /* Code blocks */
        .stCodeBlock {
            background-color: var(--secondary-bg) !important;
            border-radius: 8px !important;
            border: 1px solid var(--border-color) !important;
        }

        /* Sidebar */
        .css-1d391kg {
            background-color: var(--secondary-bg);
        }

        /* Custom select boxes */
        .stSelectbox select {
            background-color: var(--secondary-bg) !important;
            color: var(--text-color) !important;
            border-radius: 6px !important;
            border: 1px solid var(--border-color) !important;
        }

        /* Tooltips */
        .tooltip {
            position: relative;
            display: inline-block;
        }

        .tooltip .tooltiptext {
            visibility: hidden;
            background-color: var(--secondary-bg);
            color: var(--text-color);
            text-align: center;
            padding: 5px 10px;
            border-radius: 6px;
            border: 1px solid var(--border-color);
            
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
            
            opacity: 0;
            transition: opacity 0.3s;
        }

        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }

        /* Loading animations */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: var(--accent-color);
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
    """
