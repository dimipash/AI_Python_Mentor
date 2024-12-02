def get_github_dark_theme():
    return """
    <style>
        /* GitHub Dark Theme Colors */
        :root {
            --color-canvas-default: #0d1117;
            --color-canvas-subtle: #161b22;
            --color-border-default: #30363d;
            --color-border-muted: #21262d;
            --color-accent-primary: #7ee787;
            --color-accent-secondary: #58a6ff;
            --color-accent-tertiary: #f778ba;
            --color-fg-default: #c9d1d9;
            --color-fg-muted: #8b949e;
            --color-success-fg: #3fb950;
            --color-danger-fg: #f85149;
            --color-attention-fg: #d29922;
            --color-header-bg: #010409;
            --color-btn-primary-bg: #238636;
            --color-btn-primary-hover-bg: #2ea043;
        }

        /* Base Styles */
        .stApp {
            background-color: var(--color-canvas-default) !important;
            color: var(--color-fg-default) !important;
        }

        /* Header & Navigation */
        .nav-container {
            background-color: var(--color-header-bg);
            border-bottom: 1px solid var(--color-border-default);
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }

        .nav-link {
            color: var(--color-accent-secondary) !important;
            text-decoration: none;
            margin-left: 1.5rem;
            font-weight: 500;
            transition: color 0.2s ease;
        }

        .nav-link:hover {
            color: var(--color-accent-primary) !important;
        }

        /* Cards and Containers */
        .content-card {
            background-color: var(--color-canvas-subtle);
            border: 1px solid var(--color-border-default);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .progress-container {
            background-color: var(--color-canvas-subtle);
            border-radius: 8px;
            padding: 2rem;
            margin: 1rem 0;
            border: 1px solid var(--color-border-muted);
        }

        /* Buttons */
        .stButton button {
            background-color: var(--color-btn-primary-bg) !important;
            color: #ffffff !important;
            border-radius: 6px !important;
            border: 1px solid rgba(240,246,252,0.1) !important;
            padding: 8px 20px !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            text-transform: none !important;
        }

        .stButton button:hover {
            background-color: var(--color-btn-primary-hover-bg) !important;
            border-color: rgba(240,246,252,0.2) !important;
            transform: translateY(-1px);
        }

        /* Chat Messages */
        .chat-message {
            padding: 1rem 1.5rem;
            margin: 8px 0;
            border-radius: 8px;
            line-height: 1.5;
        }

        .user-message {
            background-color: rgba(88, 166, 255, 0.1);
            border: 1px solid var(--color-border-muted);
            margin-left: 2rem;
        }

        .assistant-message {
            background-color: rgba(126, 231, 135, 0.1);
            border: 1px solid var(--color-border-muted);
            margin-right: 2rem;
        }

        /* Code Blocks */
        .stCodeBlock {
            background-color: var(--color-header-bg) !important;
            border: 1px solid var(--color-border-default) !important;
            border-radius: 8px !important;
            padding: 1rem !important;
        }

        /* Progress Bars */
        .stProgress > div > div {
            background-color: var(--color-accent-primary) !important;
            transition: width 0.3s ease !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: var(--color-header-bg) !important;
            border-right: 1px solid var(--color-border-default);
            padding: 2rem 1rem;
        }

        /* Inputs */
        .stTextInput input, .stTextArea textarea {
            background-color: var(--color-canvas-subtle) !important;
            border: 1px solid var(--color-border-default) !important;
            color: var(--color-fg-default) !important;
            border-radius: 6px !important;
            padding: 0.75rem !important;
            transition: border-color 0.2s ease !important;
        }

        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: var(--color-accent-secondary) !important;
            box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.1) !important;
        }

        /* Select boxes */
        .stSelectbox select {
            background-color: var(--color-canvas-subtle) !important;
            border: 1px solid var(--color-border-default) !important;
            color: var(--color-fg-default) !important;
            border-radius: 6px !important;
            padding: 0.75rem !important;
            cursor: pointer !important;
        }

        .stSelectbox select:hover {
            border-color: var(--color-accent-secondary) !important;
        }

        /* Metrics */
        [data-testid="stMetricValue"] {
            color: var(--color-accent-primary) !important;
            font-weight: 600 !important;
        }

        /* Headers */
        h1, h2, h3 {
            color: var(--color-fg-default) !important;
            font-weight: 600 !important;
        }

        /* Links */
        a {
            color: var(--color-accent-secondary) !important;
            text-decoration: none !important;
            transition: color 0.2s ease !important;
        }

        a:hover {
            color: var(--color-accent-primary) !important;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background-color: var(--color-canvas-subtle) !important;
            border-radius: 8px !important;
            padding: 0.5rem !important;
        }

        .stTabs [data-baseweb="tab"] {
            color: var(--color-fg-muted) !important;
            border-radius: 6px !important;
            padding: 0.5rem 1rem !important;
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: var(--color-canvas-default) !important;
            color: var(--color-accent-primary) !important;
        }
    </style>
    """
