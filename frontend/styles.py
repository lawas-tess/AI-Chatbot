"""
styles.py - CSS Styles for InTurn.AI
Separated for cleaner codebase organization.
"""

def get_dark_theme_css():
    """Returns CSS variables for dark theme"""
    return """
    :root {
        --bg-primary: #030712;
        --bg-secondary: #0a0f1a;
        --bg-card: rgba(15, 23, 42, 0.6);
        --bg-card-hover: rgba(30, 41, 59, 0.8);
        --accent-primary: #3b82f6;
        --accent-secondary: #8b5cf6;
        --accent-tertiary: #06b6d4;
        --accent-glow: rgba(59, 130, 246, 0.5);
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --border-color: rgba(148, 163, 184, 0.1);
        --border-glow: rgba(59, 130, 246, 0.3);
        --sidebar-bg: linear-gradient(180deg, rgba(10, 15, 30, 0.95) 0%, rgba(5, 10, 20, 0.98) 100%);
        --app-bg-gradient1: rgba(59, 130, 246, 0.15);
        --app-bg-gradient2: rgba(139, 92, 246, 0.1);
        --input-bg: rgba(15, 23, 42, 0.8);
        --hero-bg: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.4));
        --stat-value-gradient: linear-gradient(135deg, #f8fafc, #3b82f6);
        --nav-hover-bg: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.15));
    }
    """


def get_light_theme_css():
    """Returns CSS variables for light theme"""
    return """
    :root {
        --bg-primary: #f8fafc;
        --bg-secondary: #e2e8f0;
        --bg-card: rgba(255, 255, 255, 0.95);
        --bg-card-hover: rgba(241, 245, 249, 1);
        --accent-primary: #2563eb;
        --accent-secondary: #7c3aed;
        --accent-tertiary: #0891b2;
        --accent-glow: rgba(37, 99, 235, 0.35);
        --text-primary: #0f172a;
        --text-secondary: #334155;
        --text-muted: #475569;
        --border-color: rgba(37, 99, 235, 0.4);
        --border-glow: rgba(37, 99, 235, 0.5);
        --sidebar-bg: linear-gradient(180deg, #ffffff 0%, #f1f5f9 100%);
        --app-bg-gradient1: rgba(37, 99, 235, 0.06);
        --app-bg-gradient2: rgba(124, 58, 237, 0.04);
        --input-bg: #ffffff;
        --hero-bg: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        --stat-value-gradient: linear-gradient(135deg, #0f172a, #2563eb);
        --nav-hover-bg: rgba(37, 99, 235, 0.15);
        --button-border: linear-gradient(135deg, #2563eb, #7c3aed);
    }
    
    /* Light mode specific button styling with gradient borders */
    .stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]) {
        background: white !important;
        border: 2px solid transparent !important;
        background-image: linear-gradient(white, white), linear-gradient(135deg, #2563eb, #7c3aed) !important;
        background-origin: border-box !important;
        background-clip: padding-box, border-box !important;
    }
    
    .stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]):hover {
        background: #f8fafc !important;
        background-image: linear-gradient(#f8fafc, #f8fafc), linear-gradient(135deg, #2563eb, #7c3aed) !important;
        background-origin: border-box !important;
        background-clip: padding-box, border-box !important;
    }
    
    /* Input fields with gradient borders in light mode */
    .stNumberInput > div > div > input,
    .stDateInput [data-baseweb="input"],
    .stSelectbox [data-baseweb="select"] > div,
    .stMultiSelect [data-baseweb="select"] > div,
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 2px solid transparent !important;
        background-image: linear-gradient(white, white), linear-gradient(135deg, #2563eb, #7c3aed) !important;
        background-origin: border-box !important;
        background-clip: padding-box, border-box !important;
    }
    
    /* Chat input - white inside with gradient border in light mode */
    [data-testid="stBottom"] [data-baseweb="textarea"],
    [data-testid="stChatInput"] [data-baseweb="textarea"] {
        background: white !important;
        background-image: linear-gradient(white, white), linear-gradient(135deg, #2563eb, #7c3aed) !important;
        background-origin: border-box !important;
        background-clip: padding-box, border-box !important;
    }
    
    [data-testid="stBottom"] textarea,
    [data-testid="stChatInput"] textarea {
        background: white !important;
        color: #0f172a !important;
    }
    """


def get_base_css():
    """Returns the main CSS styles (shared between themes)"""
    return """
    /* ═══ IMPORTS & VARIABLES ═══ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* ═══ GLOBAL RESET ═══ */
    .stApp {
        background: var(--bg-primary);
        background-image: 
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(59, 130, 246, 0.15), transparent),
            radial-gradient(ellipse 60% 40% at 100% 100%, rgba(139, 92, 246, 0.1), transparent);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* ═══ HIDE STREAMLIT DEFAULTS ═══ */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem; max-width: 1400px;}
    
    /* ═══ SIDEBAR - ALWAYS VISIBLE (Hide ALL collapse buttons) ═══ */
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    button[kind="headerNoPadding"],
    [data-testid="baseButton-headerNoPadding"],
    .st-emotion-cache-1rtdyuf,
    .st-emotion-cache-eczf16,
    .st-emotion-cache-2x5h05,
    .emntfgb2,
    [data-testid="stSidebar"] button[kind="headerNoPadding"],
    .stSidebarCollapseButton,
    [data-testid="stSidebar"] > div > button:first-child {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        pointer-events: none !important;
    }
    
    /* ═══ SIDEBAR - GLASS MORPHISM ═══ */
    [data-testid="stSidebar"] {
        background: var(--sidebar-bg) !important;
        background-color: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        position: relative;
        min-width: 280px !important;
        width: 280px !important;
        transform: none !important;
        transition: none !important;
    }
    
    /* Force sidebar to always be visible */
    [data-testid="stSidebar"][aria-expanded="true"],
    [data-testid="stSidebar"][aria-expanded="false"] {
        min-width: 280px !important;
        width: 280px !important;
        transform: translateX(0) !important;
        visibility: visible !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0;
        background: transparent !important;
    }
    
    [data-testid="stSidebarContent"] {
        background: transparent !important;
    }
    
    /* ═══ BRAND LOGO ═══ */
    .brand-container {
        padding: 1.5rem 1rem;
        text-align: center;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 1rem;
    }
    
    .brand-logo {
        font-size: 1.75rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0.25rem;
    }
    
    .brand-logo .brand-in {
        color: var(--text-primary);
    }
    
    .brand-logo .brand-turn {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .brand-logo .brand-ai {
        color: var(--accent-tertiary);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9em;
    }
    
    .brand-tagline {
        color: var(--text-muted);
        font-size: 0.75rem;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    /* ═══ NAVIGATION ═══ */
    .nav-section {
        padding: 0 0.75rem;
    }
    
    .nav-label {
        color: var(--text-muted);
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        padding: 0.5rem 0.75rem;
        margin-bottom: 0.25rem;
    }
    
    /* ═══ BUTTONS - MODERN STYLE ═══ */
    .stButton > button {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        padding: 0.65rem 1rem !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-align: left !important;
    }
    
    .stButton > button p,
    .stButton > button span {
        color: inherit !important;
    }
    
    .stButton > button:hover {
        background: var(--bg-card-hover) !important;
        border-color: var(--border-glow) !important;
        color: var(--text-primary) !important;
        transform: translateX(4px);
        box-shadow: 0 0 20px var(--accent-glow) !important;
    }
    
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 20px var(--accent-glow) !important;
    }
    
    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] span,
    .stButton > button[data-testid="baseButton-primary"] p,
    .stButton > button[data-testid="baseButton-primary"] span {
        color: white !important;
    }
    
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {
        transform: translateY(-2px) translateX(0) !important;
        box-shadow: 0 8px 30px var(--accent-glow) !important;
        color: white !important;
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important;
    }
    
    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="baseButton-secondary"] {
        color: var(--text-secondary) !important;
        background: var(--bg-card) !important;
    }
    
    .stButton > button[kind="secondary"]:hover,
    .stButton > button[data-testid="baseButton-secondary"]:hover {
        color: var(--text-primary) !important;
        background: var(--bg-card-hover) !important;
    }
    
    /* Sidebar specific button overrides */
    [data-testid="stSidebar"] .stButton > button {
        color: var(--text-secondary) !important;
    }
    
    [data-testid="stSidebar"] .stButton > button p,
    [data-testid="stSidebar"] .stButton > button span {
        color: inherit !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        color: var(--text-primary) !important;
    }
    
    [data-testid="stSidebar"] .stButton > button[kind="primary"],
    [data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"] {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stButton > button[kind="primary"] p,
    [data-testid="stSidebar"] .stButton > button[kind="primary"] span,
    [data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"] p,
    [data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"] span {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover,
    [data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"]:hover {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover p,
    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover span,
    [data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"]:hover p,
    [data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"]:hover span {
        color: white !important;
    }
    
    /* ═══ HERO SECTION ═══ */
    .hero-container {
        position: relative;
        padding: 3rem 2.5rem;
        border-radius: 24px;
        background: var(--hero-bg);
        border: 1px solid var(--border-color);
        margin-bottom: 2rem;
        overflow: hidden;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--accent-primary), var(--accent-secondary), transparent);
    }
    
    .hero-container::after {
        content: '';
        position: absolute;
        top: -100px;
        right: -100px;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(139, 92, 246, 0.1));
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 100px;
        padding: 0.4rem 1rem;
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--accent-primary);
        margin-bottom: 1rem;
    }
    
    .hero-badge-dot {
        width: 6px;
        height: 6px;
        background: var(--accent-tertiary);
        border-radius: 50%;
        animation: pulse-dot 2s ease-in-out infinite;
    }
    
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
    }
    
    .hero-title {
        font-size: 2.75rem;
        font-weight: 800;
        letter-spacing: -1px;
        line-height: 1.1;
        margin-bottom: 0.75rem;
        color: var(--text-primary);
    }
    
    .hero-title-gradient {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary), var(--accent-tertiary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        color: var(--text-secondary);
        font-size: 1.1rem;
        font-weight: 400;
        max-width: 600px;
        line-height: 1.6;
    }
    
    /* ═══ STATS GRID ═══ */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .stat-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 1.25rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .stat-card:hover {
        background: var(--bg-card-hover);
        border-color: var(--border-glow);
        transform: translateY(-4px);
    }
    
    .stat-card:hover::before {
        opacity: 1;
    }
    
    .stat-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .stat-value {
        font-size: 1.75rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--text-primary), var(--accent-primary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.25rem;
    }
    
    .stat-label {
        color: var(--text-muted);
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    /* ═══ FEATURE CARDS ═══ */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.25rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 1.75rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        height: 220px;
        box-sizing: border-box;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(139, 92, 246, 0.02));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: var(--border-glow);
        transform: translateY(-6px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3), 0 0 40px rgba(59, 130, 246, 0.1);
    }
    
    .feature-card:hover::before {
        opacity: 1;
    }
    
    .feature-icon-container {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.1));
        border: 1px solid rgba(59, 130, 246, 0.2);
        flex-shrink: 0;
    }
    
    .feature-title {
        color: var(--text-primary);
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        flex-shrink: 0;
    }
    
    .feature-desc {
        color: var(--text-secondary);
        font-size: 0.875rem;
        line-height: 1.6;
        margin-bottom: 1rem;
        flex-grow: 1;
        overflow: hidden;
    }
    
    .feature-link {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        color: var(--accent-primary);
        font-size: 0.85rem;
        font-weight: 600;
        cursor: pointer;
        transition: gap 0.2s ease;
        margin-top: auto;
        flex-shrink: 0;
    }
    
    .feature-link:hover {
        gap: 10px;
    }
    
    /* ═══ GLASS PANEL ═══ */
    .glass-panel {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .glass-panel-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .glass-panel-icon {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.1));
        font-size: 1.1rem;
    }
    
    .glass-panel-title {
        color: var(--text-primary);
        font-size: 1rem;
        font-weight: 600;
    }
    
    /* ═══ PROGRESS BAR - MODERN ═══ */
    .progress-wrapper {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .progress-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .progress-title {
        color: var(--text-primary);
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    .progress-percentage {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        font-size: 1.25rem;
    }
    
    .progress-track {
        height: 8px;
        background: rgba(148, 163, 184, 0.1);
        border-radius: 100px;
        overflow: hidden;
        position: relative;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary), var(--accent-tertiary));
        border-radius: 100px;
        transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    
    .progress-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .progress-stats {
        display: flex;
        justify-content: space-between;
        margin-top: 0.75rem;
    }
    
    .progress-stat {
        color: var(--text-muted);
        font-size: 0.8rem;
    }
    
    .progress-stat-value {
        color: var(--text-secondary);
        font-weight: 600;
    }
    
    /* ═══ CHAT INTERFACE ═══ */
    .chat-container {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        overflow: hidden;
    }
    
    .chat-header {
        background: var(--bg-card);
        padding: 1rem 1.5rem;
        border-bottom: 1px solid var(--border-color);
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .chat-status {
        width: 8px;
        height: 8px;
        background: #22c55e;
        border-radius: 50%;
        box-shadow: 0 0 10px rgba(34, 197, 94, 0.5);
    }
    
    .chat-title {
        color: var(--text-primary);
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    /* ═══ SUGGESTION CHIPS ═══ */
    .suggestion-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
        margin: 1rem 0;
    }
    
    .suggestion-chip {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
    }
    
    .suggestion-chip:hover {
        background: var(--bg-card-hover);
        border-color: var(--border-glow);
        transform: scale(1.02);
    }
    
    .suggestion-icon {
        font-size: 1.25rem;
        flex-shrink: 0;
    }
    
    .suggestion-text {
        color: var(--text-secondary);
        font-size: 0.875rem;
        line-height: 1.5;
    }
    
    /* ═══ CATEGORY TABS ═══ */
    .category-container {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
        padding: 0.5rem;
        background: var(--bg-card);
        border-radius: 12px;
        border: 1px solid var(--border-color);
    }
    
    .category-tab {
        padding: 0.6rem 1.25rem;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 500;
        color: var(--text-muted);
        cursor: pointer;
        transition: all 0.2s ease;
        border: 1px solid transparent;
    }
    
    .category-tab:hover {
        color: var(--text-secondary);
        background: rgba(59, 130, 246, 0.1);
    }
    
    .category-tab.active {
        color: var(--text-primary);
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.15));
        border-color: var(--border-glow);
    }
    
    /* ═══ REPORT SECTION ═══ */
    .report-container {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        overflow: hidden;
    }
    
    .report-header {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.05));
        padding: 1.5rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .report-body {
        padding: 1.5rem;
    }
    
    .report-output {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        color: var(--text-secondary);
        line-height: 1.8;
        font-size: 0.95rem;
    }
    
    /* ═══ TIP CARDS ═══ */
    .tip-card {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(139, 92, 246, 0.04));
        border: 1px solid rgba(59, 130, 246, 0.15);
        border-left: 3px solid var(--accent-primary);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    
    .tip-label {
        color: var(--accent-primary);
        font-weight: 600;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.35rem;
    }
    
    /* ═══ FORM INPUTS ═══ */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: var(--input-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-size: 0.95rem !important;
        padding: 0.75rem 1rem !important;
        caret-color: var(--accent-primary) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
    }
    
    .stSelectbox > div > div {
        background: var(--input-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
    }
    
    /* Selectbox text and arrow visibility */
    .stSelectbox [data-baseweb="select"] > div {
        background: var(--input-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
    }
    
    .stSelectbox [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] div[data-baseweb="select-value-container"] {
        color: var(--text-primary) !important;
    }
    
    /* Selectbox input text - for typing/filtering */
    .stSelectbox input,
    .stSelectbox [data-baseweb="select"] input,
    [data-baseweb="select"] input,
    [data-baseweb="input"] input,
    [data-baseweb="combobox"] input {
        color: var(--text-primary) !important;
        background: transparent !important;
        caret-color: var(--text-primary) !important;
        -webkit-text-fill-color: var(--text-primary) !important;
    }
    
    .stSelectbox input::placeholder,
    [data-baseweb="select"] input::placeholder {
        color: var(--text-muted) !important;
        -webkit-text-fill-color: var(--text-muted) !important;
    }
    
    /* Dropdown arrow - force visibility */
    .stSelectbox svg,
    .stSelectbox [data-baseweb="select"] svg,
    .stSelectbox [data-baseweb="icon"] svg,
    [data-baseweb="select"] [data-baseweb="icon"],
    [data-baseweb="select"] svg {
        fill: var(--text-primary) !important;
        color: var(--text-primary) !important;
        stroke: var(--text-primary) !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* Dropdown menu styling */
    [data-baseweb="popover"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
    }
    
    [data-baseweb="menu"] {
        background: var(--bg-card) !important;
    }
    
    [data-baseweb="menu"] li {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
    }
    
    [data-baseweb="menu"] li:hover {
        background: var(--bg-card-hover) !important;
    }
    
    /* ═══ NUMBER INPUT ═══ */
    .stNumberInput > div > div > input {
        background: var(--input-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        -webkit-text-fill-color: var(--text-primary) !important;
    }
    
    .stNumberInput button {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
        transition: all 0.15s ease !important;
    }
    
    .stNumberInput button svg {
        fill: var(--text-primary) !important;
        stroke: var(--text-primary) !important;
        transition: all 0.15s ease !important;
    }
    
    /* Minus button - red on hover */
    .stNumberInput button:first-of-type:hover {
        background: #dc2626 !important;
        border-color: #dc2626 !important;
    }
    
    .stNumberInput button:first-of-type:hover svg {
        fill: white !important;
        stroke: white !important;
    }
    
    /* Plus button - black on hover */
    .stNumberInput button:last-of-type:hover {
        background: #0f172a !important;
        border-color: #0f172a !important;
    }
    
    .stNumberInput button:last-of-type:hover svg {
        fill: white !important;
        stroke: white !important;
    }
    
    /* ═══ DATE INPUT ═══ */
    .stDateInput > div > div > input,
    [data-baseweb="input"] input {
        background: var(--input-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        -webkit-text-fill-color: var(--text-primary) !important;
    }
    
    .stDateInput [data-baseweb="input"] {
        background: var(--input-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
    }
    
    /* Date picker calendar */
    [data-baseweb="calendar"] {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
    }
    
    [data-baseweb="calendar"] div {
        color: var(--text-primary) !important;
    }
    
    /* ═══ LABELS ═══ */
    .stTextInput label, .stTextArea label, .stSelectbox label,
    .stNumberInput label, .stDateInput label, .stMultiSelect label {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* ═══ MULTISELECT ═══ */
    .stMultiSelect [data-baseweb="select"] > div {
        background: var(--input-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
    }
    
    .stMultiSelect [data-baseweb="tag"] {
        background: #dc2626 !important;
        color: white !important;
    }
    
    .stMultiSelect [data-baseweb="tag"] span {
        color: white !important;
    }
    
    .stMultiSelect [data-baseweb="tag"] svg {
        fill: white !important;
    }
    
    /* Clear all and Open buttons */
    .stMultiSelect span[data-baseweb="tag"] ~ span,
    .stMultiSelect [data-baseweb="select"] span:not([data-baseweb="tag"]),
    [data-baseweb="popover"] span,
    [data-baseweb="select"] > div > div:last-child span {
        color: var(--text-primary) !important;
    }
    
    /* Clear all / Open links */
    .stMultiSelect a,
    .stMultiSelect button span,
    [data-baseweb="select"] a {
        color: var(--accent-primary) !important;
    }
    
    /* ═══ DOWNLOAD BUTTON ═══ */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669, #10b981) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(16, 185, 129, 0.4) !important;
    }
    
    /* ═══ CHAT MESSAGE OVERRIDE ═══ */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        padding: 0.5rem 0 !important;
    }
    
    [data-testid="stChatMessageContent"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 16px !important;
        padding: 1rem 1.25rem !important;
    }
    
    /* ═══ USER MESSAGE ═══ */
    [data-testid="stChatMessage"][data-testid*="user"] [data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important;
        border: none !important;
        color: white !important;
    }
    
    /* ═══ EXPANDER ═══ */
    .streamlit-expanderHeader,
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] summary p {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stExpander"] summary {
        position: relative !important;
        padding-right: 2.5rem !important;
    }
    
    /* Arrow indicator on right */
    [data-testid="stExpander"] summary::after {
        content: '▼' !important;
        position: absolute !important;
        right: 1rem !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        font-size: 10px !important;
        color: var(--text-muted) !important;
        transition: transform 0.2s ease !important;
    }
    
    [data-testid="stExpander"][open] summary::after {
        transform: translateY(-50%) rotate(180deg) !important;
    }
    
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] summary p {
        background: transparent !important;
        border: none !important;
    }
    
    /* Hide default Streamlit arrow */
    [data-testid="stExpander"] summary svg {
        display: none !important;
    }
    
    .streamlit-expanderContent,
    [data-testid="stExpander"] > div[data-testid="stExpanderDetails"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
    }
    
    /* ═══ DIVIDER ═══ */
    .gradient-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-glow), transparent);
        margin: 2rem 0;
    }
    
    /* ═══ FOOTER ═══ */
    .sidebar-footer {
        text-align: center;
        padding: 1.5rem 1rem;
        border-top: 1px solid var(--border-color);
        margin-top: auto;
    }
    
    .footer-text {
        color: var(--text-muted);
        font-size: 0.7rem;
    }
    
    /* ═══ ANIMATIONS ═══ */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-in {
        animation: fadeInUp 0.5s ease forwards;
    }
    
    /* ═══ SCROLLBAR ═══ */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--accent-primary), var(--accent-secondary));
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #60a5fa, #a78bfa);
    }
    
    /* ═══ RESPONSIVE ═══ */
    @media (max-width: 768px) {
        .stats-grid, .feature-grid {
            grid-template-columns: 1fr;
        }
        .suggestion-grid {
            grid-template-columns: 1fr;
        }
        .hero-title {
            font-size: 2rem;
        }
    }
    
    /* ═══ LIGHT MODE SPECIFIC FIXES ═══ */
    .hero-container {
        background: var(--hero-bg, linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.4)));
    }
    
    .stat-value {
        background: var(--stat-value-gradient, linear-gradient(135deg, var(--text-primary), var(--accent-primary)));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stButton > button:hover {
        background: var(--nav-hover-bg, linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.15))) !important;
        color: var(--text-primary) !important;
    }
    
    /* Chat header for light mode */
    .chat-header {
        background: var(--bg-secondary) !important;
    }
    
    /* Report output for light mode */
    .report-output {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
    }
    
    /* Feature card icon for light mode */
    .feature-icon-container {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.15), rgba(124, 58, 237, 0.1)) !important;
    }
    
    /* Suggestion chip text for light mode */
    .suggestion-text {
        color: var(--text-secondary) !important;
    }
    
    /* Progress track for light mode */
    .progress-track {
        background: var(--border-color) !important;
    }
    
    /* ═══ CHAT INPUT - AT BOTTOM OF CONTENT ═══ */
    [data-testid="stBottom"] {
        position: relative !important;
        background: transparent !important;
        border: none !important;
        padding: 1rem 0 !important;
        margin-top: 2rem !important;
    }
    
    /* Reset nested containers */
    [data-testid="stBottom"] > div,
    [data-testid="stBottom"] [data-testid="stChatInput"],
    [data-testid="stBottom"] [data-testid="stChatInput"] > div,
    [data-testid="stBottom"] [data-testid="stChatInputContainer"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Main chat input wrapper - gradient border */
    [data-testid="stBottom"] [data-baseweb="textarea"],
    [data-testid="stChatInput"] [data-baseweb="textarea"] {
        background: var(--bg-card) !important;
        border: 2px solid transparent !important;
        background-image: linear-gradient(var(--bg-card), var(--bg-card)), linear-gradient(135deg, #2563eb, #7c3aed) !important;
        background-origin: border-box !important;
        background-clip: padding-box, border-box !important;
        border-radius: 12px !important;
        box-shadow: none !important;
    }
    
    /* Remove any gradient borders from Streamlit */
    [data-testid="stBottom"] [data-baseweb="textarea"]::before,
    [data-testid="stBottom"] [data-baseweb="textarea"]::after,
    [data-testid="stChatInput"]::before,
    [data-testid="stChatInput"]::after,
    [data-testid="stBottom"] > div::before,
    [data-testid="stBottom"] > div::after {
        display: none !important;
        content: none !important;
    }
    
    /* Chat input textarea styling */
    [data-testid="stBottom"] textarea,
    [data-testid="stChatInput"] textarea {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: none !important;
        border-radius: 12px !important;
        caret-color: var(--accent-primary) !important;
        padding: 14px 50px 14px 16px !important;
        font-size: 15px !important;
    }
    
    [data-testid="stBottom"] textarea::placeholder,
    [data-testid="stChatInput"] textarea::placeholder {
        color: var(--text-muted) !important;
        opacity: 0.7 !important;
    }
    
    /* Focus state */
    [data-testid="stBottom"] textarea:focus,
    [data-testid="stChatInput"] textarea:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    [data-testid="stBottom"] [data-baseweb="textarea"]:focus-within {
        border-color: var(--accent-primary) !important;
    }
    
    /* Send button styling - RED */
    [data-testid="stChatInput"] button,
    [data-testid="stBottom"] button,
    [data-testid="stChatInputContainer"] button {
        background: #dc2626 !important;
        border: none !important;
        border-radius: 8px !important;
        color: white !important;
        min-width: 36px !important;
        min-height: 36px !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    [data-testid="stChatInput"] button svg,
    [data-testid="stBottom"] button svg {
        fill: white !important;
        color: white !important;
    }
    
    [data-testid="stChatInput"] button:hover,
    [data-testid="stBottom"] button:hover {
        background: #b91c1c !important;
    }
    
    /* No extra padding needed since not fixed */
    [data-testid="stMain"] .block-container {
        padding-bottom: 2rem !important;
    }
    
    /* Suggestion chips hover fix */
    .suggestion-chip:hover {
        background: var(--bg-card-hover) !important;
    }
    
    .suggestion-chip:hover .suggestion-text {
        color: var(--text-primary) !important;
    }
    
    /* Stat cards - ensure visibility */
    .stat-card {
        background: var(--bg-card) !important;
    }
    
    .stat-label {
        color: var(--text-muted) !important;
    }
    """


def get_full_css(is_dark_mode: bool) -> str:
    """
    Returns the complete CSS string based on the current theme.
    
    Args:
        is_dark_mode: True for dark theme, False for light theme
    
    Returns:
        Complete CSS string ready to be injected via st.markdown
    """
    theme_css = get_dark_theme_css() if is_dark_mode else get_light_theme_css()
    base_css = get_base_css()
    
    return f"""
<style>
    {theme_css}
    {base_css}
</style>
"""
