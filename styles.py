def get_github_dark_theme():
    return """
    <style>
        /* GitHub Dark Theme Colors */
        :root {
            --color-canvas-default: #0d1117;
            --color-canvas-subtle: #161b22;
            --color-border-default: #30363d;
            --color-border-muted: #21262d;
            --color-accent-fg: #58a6ff;
            --color-fg-default: #c9d1d9;
            --color-fg-muted: #8b949e;
            --color-success-fg: #3fb950;
            --color-danger-fg: #f85149;
            --color-attention-fg: #d29922;
        }

        /* Base Styles */
        .stApp {
            background-color: var(--color-canvas-default);
            color: var(--color-fg-default);
        }

        /* Header & Navigation */
        .nav-container {
            background-color: var(--color-canvas-subtle);
            border-bottom: 1px solid var(--color-border-default);
            padding: 1rem;
            margin-bottom: 1.5rem;
        }

        /* Cards */
        .content-card {
            background-color: var(--color-canvas-subtle);
            border: 1px solid var(--color-border-default);
            border-radius: 6px;
            padding: 1rem;
            margin: 1rem 0;
        }

        /* Buttons */
        .stButton button {
            background-color: #238636 !important;
            color: #ffffff !important;
            border-radius: 6px !important;
            border: 1px solid rgba(240,246,252,0.1) !important;
            padding: 5px 16px !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
        }

        .stButton button:hover {
            background-color: #2ea043 !important;
        }

        /* Chat Messages */
        .chat-message {
            padding: 8px 16px;
            margin: 4px 0;
            border-radius: 6px;
        }

        .user-message {
            background-color: var(--color-canvas-subtle);
            border: 1px solid var(--color-border-muted);
            margin-left: 24px;
        }

        .assistant-message {
            background-color: rgba(88, 166, 255, 0.1);
            border: 1px solid var(--color-border-muted);
            margin-right: 24px;
        }

        /* Code Blocks */
        .stCodeBlock {
            background-color: var(--color-canvas-subtle) !important;
            border: 1px solid var(--color-border-default) !important;
            border-radius: 6px !important;
        }

        /* Progress Bars */
        .stProgress > div > div {
            background-color: var(--color-accent-fg) !important;
        }

        /* Sidebar */
        .css-1d391kg {
            background-color: var(--color-canvas-subtle);
            border-right: 1px solid var(--color-border-default);
        }

        /* Inputs */
        .stTextInput input, .stTextArea textarea {
            background-color: var(--color-canvas-subtle) !important;
            border: 1px solid var(--color-border-default) !important;
            color: var(--color-fg-default) !important;
            border-radius: 6px !important;
        }

        /* Select boxes */
        .stSelectbox select {
            background-color: var(--color-canvas-subtle) !important;
            border: 1px solid var(--color-border-default) !important;
            color: var(--color-fg-default) !important;
            border-radius: 6px !important;
        }
    </style>
    """
