import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import datetime, date
import time
from styles import get_full_css

API = "http://localhost:8001"

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="InTurn.AI | Smart Internship Assistant",
    page_icon="I",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
# THEME MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

is_dark = st.session_state.theme == "dark"

# ══════════════════════════════════════════════════════════════════════════════
# APPLY CSS STYLES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(get_full_css(is_dark), unsafe_allow_html=True)

# Scroll to top when navigating
if st.session_state.get("scroll_to_top", False):
    components.html("""
    <script>
        window.parent.document.querySelector('[data-testid="stMain"]')?.scrollTo({top: 0, behavior: 'instant'});
        window.parent.scrollTo({top: 0, behavior: 'instant'});
        const mainElement = window.parent.document.querySelector('section.main');
        if (mainElement) mainElement.scrollTop = 0;
    </script>
    """, height=0)
    st.session_state.scroll_to_top = False

# ══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════
def send_message(user_input, message_list):
    """Send a message to the API and return the AI response"""
    message_list.append({"role": "user", "content": user_input})
    try:
        history = message_list[:-1]
        res = requests.post(
            f"{API}/chat",
            json={"message": user_input, "history": history},
            timeout=30
        )
        res.raise_for_status()
        reply = res.json()["reply"]
    except requests.exceptions.Timeout:
        reply = "Request timed out. The AI is taking too long to respond."
    except requests.exceptions.ConnectionError:
        reply = "Could not connect to backend. Make sure it's running on port 8001."
    except Exception as e:
        reply = f"Error: {str(e)}"
    message_list.append({"role": "assistant", "content": reply})
    return reply

def load_chat_history(route):
    """Load saved chat history for a given route"""
    try:
        res = requests.get(f"{API}/chat_history/{route}", timeout=10)
        res.raise_for_status()
        return res.json().get("messages", [])
    except Exception:
        return []

def load_saved_reports():
    """Load saved reports from the backend"""
    try:
        res = requests.get(f"{API}/reports", timeout=10)
        res.raise_for_status()
        return res.json().get("reports", [])
    except Exception:
        return []

def save_report_entry(report_type, task_input, report_content):
    """Persist a generated report to the backend"""
    payload = {
        "report_type": report_type,
        "task_input": task_input,
        "content": report_content,
        "created_at": datetime.utcnow().isoformat()
    }
    response = requests.post(f"{API}/reports", json=payload, timeout=10)
    response.raise_for_status()
    payload["report_id"] = response.json().get("report_id")
    return payload

def delete_saved_report(report_id):
    """Delete a saved report from the backend"""
    response = requests.delete(f"{API}/reports/{report_id}", timeout=10)
    response.raise_for_status()
    return response.json().get("deleted", False)

def render_progress(current, total):
    """Render modern progress bar"""
    percent = (current / total * 100) if total > 0 else 0
    st.markdown(f"""
    <div class="progress-wrapper">
        <div class="progress-header">
            <span class="progress-title">Internship Progress</span>
            <span class="progress-percentage">{percent:.1f}%</span>
        </div>
        <div class="progress-track">
            <div class="progress-fill" style="width: {min(percent, 100)}%;"></div>
        </div>
        <div class="progress-stats">
            <span class="progress-stat"><span class="progress-stat-value">{current}</span> hours completed</span>
            <span class="progress-stat"><span class="progress-stat-value">{total - current}</span> hours remaining</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Brand Logo
    st.markdown("""
    <div class="brand-container">
        <div class="brand-logo">
            <span class="brand-in">In</span><span class="brand-turn">Turn</span><span class="brand-ai">.AI</span>
        </div>
        <div class="brand-tagline">SMART INTERNSHIP ASSISTANT</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Theme Toggle Button
    theme_label = "Switch to Light Mode" if is_dark else "Switch to Dark Mode"
    if st.button(theme_label, key="theme_toggle", use_container_width=True):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()
    
    st.markdown('<div style="height: 0.5rem;"></div>', unsafe_allow_html=True)
    
    # Initialize page state
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"
    
    # Navigation
    st.markdown('<div class="nav-section">', unsafe_allow_html=True)
    st.markdown('<div class="nav-label">Navigation</div>', unsafe_allow_html=True)
    
    nav_items = [
        ("", "Dashboard", "Home"),
        ("", "InternTrack", "Hours"),
        ("", "MentorBridge", "Chat"),
        ("", "Report Writer", "Reports")
    ]
    
    for icon, name, shortname in nav_items:
        is_active = st.session_state.page == name
        if st.button(
            name,
            key=f"nav_{name}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.page = name
            st.session_state.scroll_to_top = True
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="sidebar-footer">
        <div class="footer-text">CSIT349-G01</div>
        <div class="footer-text" style="margin-top: 4px;">© 2026 InTurn.AI</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD PAGE
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "Dashboard":
    
    # Hero Section
    current_hour = datetime.now().hour
    greeting = "Good morning" if current_hour < 12 else "Good afternoon" if current_hour < 18 else "Good evening"
    
    st.markdown(f"""
    <div class="hero-container">
        <div class="hero-badge">
            <span class="hero-badge-dot"></span>
            AI-Powered Assistant
        </div>
        <div class="hero-title">
            {greeting}, <span class="hero-title-gradient">Welcome back!</span>
        </div>
        <div class="hero-subtitle">
            Your intelligent companion for managing your internship journey. Track hours, get communication help, and generate professional reports — all in one place.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Grid
    st.markdown(f"""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--accent-primary)" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg></div>
            <div class="stat-value">3</div>
            <div class="stat-label">AI Tools</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--accent-primary)" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg></div>
            <div class="stat-value">24/7</div>
            <div class="stat-label">Available</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--accent-primary)" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg></div>
            <div class="stat-value">Fast</div>
            <div class="stat-label">Response</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--accent-primary)" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg></div>
            <div class="stat-value">{datetime.now().strftime('%b %d')}</div>
            <div class="stat-label">Today</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon-container"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--accent-primary)" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg></div>
            <div class="feature-title">InternTrack</div>
            <div class="feature-desc">Log your daily hours, track your progress, and get AI-powered insights on your internship completion timeline.</div>
            <div class="feature-link">Get Started →</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open InternTrack", key="goto_interntrack", use_container_width=True):
            st.session_state.page = "InternTrack"
            st.session_state.scroll_to_top = True
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon-container"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--accent-primary)" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg></div>
            <div class="feature-title">MentorBridge</div>
            <div class="feature-desc">Get help crafting professional messages for your supervisor. Perfect communication for any workplace situation.</div>
            <div class="feature-link">Start Chatting →</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open MentorBridge", key="goto_mentorbridge", use_container_width=True):
            st.session_state.page = "MentorBridge"
            st.session_state.scroll_to_top = True
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon-container"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--accent-primary)" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg></div>
            <div class="feature-title">Report Writer</div>
            <div class="feature-desc">Transform your tasks into polished professional reports. Supports daily, weekly, and monthly formats.</div>
            <div class="feature-link">Write Report →</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Report Writer", key="goto_reportwriter", use_container_width=True):
            st.session_state.page = "Report Writer"
            st.session_state.scroll_to_top = True
            st.rerun()
    
    # Pro Tips
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-panel">
        <div class="glass-panel-header">
            <div class="glass-panel-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--accent-tertiary)" stroke-width="2"><path d="M9 18h6"></path><path d="M10 22h4"></path><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"></path></svg></div>
            <div class="glass-panel-title">Quick Tips</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    tips = [
        ("Consistency", "Log hours daily for accurate tracking"),
        ("Preparation", "Use MentorBridge before difficult conversations"),
        ("Efficiency", "Generate reports while tasks are fresh")
    ]
    
    for label, tip in tips:
        st.markdown(f"""
        <div class="tip-card">
            <div class="tip-label">{label}</div>
            {tip}
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# INTERNTRACK PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "InternTrack":

    # Load saved config from backend once per session
    if "intern_config" not in st.session_state:
        try:
            cfg_res = requests.get(f"{API}/get_config", timeout=5)
            st.session_state.intern_config = cfg_res.json() if cfg_res.ok else {}
        except Exception:
            st.session_state.intern_config = {}
    cfg = st.session_state.intern_config

    # Hero
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">
            <span class="hero-badge-dot"></span>
            Hour Tracking
        </div>
        <div class="hero-title">
            <span class="hero-title-gradient">InternTrack</span>
        </div>
        <div class="hero-subtitle">
            Log your hours, monitor progress, and get AI-powered insights about your internship completion
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Configuration
    with st.expander("Configuration", expanded=not bool(cfg)):
        col1, col2, col3 = st.columns(3)
        with col1:
            total_hours = st.number_input("Total Required Hours", value=int(cfg.get("total_hours", 500)), min_value=1)
            current_hours = st.number_input("Current Hours", value=int(cfg.get("current_hours", 0)), min_value=0)
        with col2:
            daily_hours = st.number_input("Daily Hours", value=int(cfg.get("daily_hours", 8)), min_value=1, max_value=24)
            _saved_date = cfg.get("start_date")
            start_date = st.date_input("Start Date",
                value=date.fromisoformat(_saved_date) if _saved_date else datetime.now().date())
        with col3:
            _countries = ["Singapore", "Philippines", "USA", "Japan", "Other"]
            country = st.selectbox("Country", _countries,
                index=_countries.index(cfg["country"]) if cfg.get("country") in _countries else 0)
            days = st.multiselect("Working Days", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                                default=cfg.get("working_days", ["Mon", "Tue", "Wed", "Thu", "Fri"]))
        if st.button("Save Configuration", use_container_width=True):
            config_data = {
                "total_hours": total_hours,
                "current_hours": current_hours,
                "daily_hours": daily_hours,
                "start_date": str(start_date),
                "country": country,
                "working_days": days
            }
            try:
                requests.post(f"{API}/save_config", json=config_data, timeout=5)
                st.session_state.intern_config = config_data
                st.success("Configuration saved! The AI now knows your internship details.")
            except Exception:
                st.error("Could not save config. Make sure the backend is running.")

    render_progress(current_hours, total_hours)
    
    # Stats
    remaining = total_hours - current_hours
    days_left = remaining / daily_hours if daily_hours > 0 else 0
    
    st.markdown(f"""
    <div class="stats-grid" style="grid-template-columns: repeat(3, 1fr); margin: 1.5rem 0;">
        <div class="stat-card">
            <div class="stat-value">{current_hours}</div>
            <div class="stat-label">Hours Done</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{remaining}</div>
            <div class="stat-label">Hours Left</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">~{int(days_left)}</div>
            <div class="stat-label">Days Left</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # Chat
    st.markdown("""
    <div class="glass-panel">
        <div class="glass-panel-header">
            <div class="glass-panel-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--accent-primary)" stroke-width="2"><rect x="3" y="11" width="18" height="10" rx="2"></rect><circle cx="12" cy="5" r="2"></circle><path d="M12 7v4"></path><line x1="8" y1="16" x2="8" y2="16"></line><line x1="16" y1="16" x2="16" y2="16"></line></svg></div>
            <div class="glass-panel-title">AI Assistant</div>
            <div style="margin-left: auto; display: flex; align-items: center; gap: 6px;">
                <div class="chat-status"></div>
                <span style="color: var(--text-muted); font-size: 0.75rem;">Online</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if "interntrack_messages" not in st.session_state:
        st.session_state.interntrack_messages = []
    
    # Suggestions
    if not st.session_state.interntrack_messages:
        suggestions = [
            "Help me set up my internship tracking",
            "+8 today — completed presentation",
            "How many hours left? When will I finish?",
            "Give me a weekly progress report"
        ]
        cols = st.columns(2)
        for i, text in enumerate(suggestions):
            with cols[i % 2]:
                if st.button(text, key=f"sug_it_{i}", use_container_width=True):
                    with st.spinner("Processing..."):
                        send_message(text, st.session_state.interntrack_messages)
                    st.rerun()
    
    # Messages
    for m in st.session_state.interntrack_messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])
    
    # Input
    if user_input := st.chat_input("Ask about your hours...", key="it_input"):
        with st.spinner("Thinking..."):
            send_message(user_input, st.session_state.interntrack_messages)
        st.rerun()
    
    if st.session_state.interntrack_messages:
        if st.button("Clear Chat", key="clear_it"):
            st.session_state.interntrack_messages = []
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# MENTORBRIDGE PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "MentorBridge":
    
    # Hero
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">
            <span class="hero-badge-dot"></span>
            Communication Help
        </div>
        <div class="hero-title">
            <span class="hero-title-gradient">MentorBridge</span>
        </div>
        <div class="hero-subtitle">
            Find the right words for any workplace situation. Get AI-powered help crafting professional messages to your supervisor or mentor.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Info
    st.markdown("""
    <div class="glass-panel">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div class="glass-panel-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--accent-tertiary)" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle></svg></div>
            <div>
                <div style="color: var(--text-primary); font-weight: 600;">How it works</div>
                <div style="color: var(--text-secondary); font-size: 0.9rem;">
                    Describe your situation and I'll help you craft a professional, respectful message.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if "mentorbridge_messages" not in st.session_state:
        st.session_state.mentorbridge_messages = load_chat_history("mentorbridge")
    
    # Scenarios
    if not st.session_state.mentorbridge_messages:
        st.markdown("""
        <div style="color: var(--text-muted); font-size: 0.75rem; text-transform: uppercase; 
                    letter-spacing: 1px; margin-bottom: 1rem;">Common Scenarios</div>
        """, unsafe_allow_html=True)
        
        scenarios = [
            ("Ask for clarification", "What do I say to my supervisor when I don't understand a task?"),
            ("Request permission", "How do I ask permission to leave early?"),
            ("Admit a mistake", "How do I professionally admit I made an error?"),
            ("Discuss workload", "How do I say the workload is too much?")
        ]
        
        cols = st.columns(2)
        for i, (title, prompt) in enumerate(scenarios):
            with cols[i % 2]:
                st.markdown(f"""
                <div style="background: var(--bg-card); border: 1px solid var(--border-color);
                            border-radius: 12px; padding: 0.75rem 1rem; margin-bottom: 0.5rem;">
                    <span style="font-size: 0.75rem; color: var(--accent-primary); font-weight: 600;">
                        {title}
                    </span>
                </div>
                """, unsafe_allow_html=True)
                if st.button(prompt[:45] + "...", key=f"mb_btn_{i}", use_container_width=True, help=prompt):
                    with st.spinner("Crafting response..."):
                        send_message(prompt, st.session_state.mentorbridge_messages)
                    st.rerun()
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # Messages
    for m in st.session_state.mentorbridge_messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])
    
    # Input
    if user_input := st.chat_input("Describe your situation...", key="mb_input"):
        with st.spinner("Crafting response..."):
            send_message(user_input, st.session_state.mentorbridge_messages)
        st.rerun()
    
    if st.session_state.mentorbridge_messages:
        if st.button("Clear Chat", key="clear_mb"):
            st.session_state.mentorbridge_messages = []
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# REPORT WRITER PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Report Writer":

    if "saved_reports" not in st.session_state:
        st.session_state.saved_reports = load_saved_reports()
    
    # Hero
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">
            <span class="hero-badge-dot"></span>
            AI Report Generator
        </div>
        <div class="hero-title">
            <span class="hero-title-gradient">Report Writer</span>
        </div>
        <div class="hero-subtitle">
            Transform your daily tasks into polished professional reports. Perfect for daily, weekly, or monthly submissions.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Report Interface
    st.markdown("""
    <div class="glass-panel" style="padding: 0; overflow: hidden;">
        <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.05)); 
                    padding: 1.25rem 1.5rem; border-bottom: 1px solid var(--border-color);">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="width: 32px; height: 32px; border-radius: 8px; 
                            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
                            display: flex; align-items: center; justify-content: center; color: white; font-size: 0.9rem;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                        <line x1="16" y1="13" x2="8" y2="13"></line>
                        <line x1="16" y1="17" x2="8" y2="17"></line>
                        <polyline points="10 9 9 9 8 9"></polyline>
                    </svg>
                </div>
                <div>
                    <div style="color: var(--text-primary); font-weight: 600; font-size: 1rem;">Create New Report</div>
                    <div style="color: var(--text-muted); font-size: 0.75rem;">Select type and enter your tasks below</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Report Configuration Row
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 16px; 
                    padding: 1.5rem; margin-top: 1rem;">
            <div style="color: var(--text-secondary); font-size: 0.7rem; font-weight: 600; 
                        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;">
                Report Configuration
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        report_type = st.selectbox(
            "Report Type",
            ["Daily Report", "Weekly Report", "Monthly Report"],
            key="report_type"
        )
        
        st.markdown("""
        <div style="background: rgba(59, 130, 246, 0.08); border: 1px solid rgba(59, 130, 246, 0.15);
                    border-radius: 10px; padding: 1rem; margin-top: 1rem;">
            <div style="color: var(--accent-primary); font-size: 0.7rem; font-weight: 600; 
                        text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem;">Pro Tip</div>
            <div style="color: var(--text-secondary); font-size: 0.85rem; line-height: 1.5;">
                Be specific about tasks and include measurable outcomes for more professional reports.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="color: var(--text-secondary); font-size: 0.7rem; font-weight: 600; 
                    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem; margin-top: 1rem;">
            Task Input
            <span style="float: right; color: var(--text-muted); font-weight: 400;">One task per line</span>
        </div>
        """, unsafe_allow_html=True)
        
        task_input = st.text_area(
            "Enter tasks",
            placeholder="Attended morning standup meeting with the team\nUpdated inventory spreadsheet with Q1 data\nPrepared presentation slides for client meeting\nFiled and organized important documents\nAssisted senior developer with code review",
            height=200,
            key="task_input",
            label_visibility="collapsed"
        )
    
    # Generate Button
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate = st.button("Generate Report", use_container_width=True, type="primary")
    
    if generate:
        if not task_input.strip():
            st.warning("Please enter your tasks before generating a report.")
        else:
            message = f"Generate a professional {report_type} for these tasks:\n{task_input}"
            
            with st.spinner("Generating your report..."):
                try:
                    res = requests.post(f"{API}/chat", json={"message": message}, timeout=30)
                    res.raise_for_status()
                    report = res.json()["reply"]
                    saved_report = save_report_entry(report_type, task_input, report)
                    st.session_state.saved_reports = [saved_report] + st.session_state.saved_reports
                    
                    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
                    
                    # Report Output Header
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(16, 185, 129, 0.05));
                                border: 1px solid rgba(34, 197, 94, 0.2); border-radius: 12px; 
                                padding: 1rem 1.25rem; margin-bottom: 1.5rem;">
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <div style="width: 28px; height: 28px; border-radius: 50%; background: rgba(34, 197, 94, 0.2);
                                        display: flex; align-items: center; justify-content: center;">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="3">
                                    <polyline points="20 6 9 17 4 12"></polyline>
                                </svg>
                            </div>
                            <div style="color: #22c55e; font-weight: 600; font-size: 0.9rem;">Report generated successfully</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Report Content
                    st.markdown(f"""
                    <div style="background: var(--bg-card); border: 1px solid var(--border-color); 
                                border-radius: 16px; overflow: hidden; margin-bottom: 1.5rem;">
                        <div style="background: var(--bg-secondary); padding: 1rem 1.5rem; 
                                    border-bottom: 1px solid var(--border-color);
                                    display: flex; justify-content: space-between; align-items: center;">
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent-primary)" stroke-width="2">
                                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                                    <polyline points="14 2 14 8 20 8"></polyline>
                                </svg>
                                <span style="color: var(--text-primary); font-weight: 600;">{report_type}</span>
                            </div>
                            <span style="color: var(--text-muted); font-size: 0.8rem;">{datetime.now().strftime('%B %d, %Y')}</span>
                        </div>
                        <div style="padding: 1.5rem; color: var(--text-secondary); line-height: 1.8;">
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(report)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Download Options
                    st.markdown("""
                    <div style="color: var(--text-muted); font-size: 0.7rem; font-weight: 600; 
                                text-transform: uppercase; letter-spacing: 1px; margin: 1.5rem 0 0.75rem 0;">
                        Export Options
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            "Download as TXT",
                            report,
                            f"{report_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                            "text/plain",
                            use_container_width=True
                        )
                    with col2:
                        md = f"# {report_type}\n**Date:** {datetime.now().strftime('%B %d, %Y')}\n\n---\n\n{report}"
                        st.download_button(
                            "Download as Markdown",
                            md,
                            f"{report_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md",
                            "text/markdown",
                            use_container_width=True
                        )
                        
                except requests.exceptions.Timeout:
                    st.error("Request timed out. Please try again.")
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to backend. Make sure it's running.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    if st.session_state.saved_reports:
        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="color: var(--text-muted); font-size: 0.7rem; font-weight: 600;
                    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;">
            Saved Reports
        </div>
        """, unsafe_allow_html=True)

        for index, saved_report in enumerate(st.session_state.saved_reports[:5]):
            created_at = saved_report.get("created_at", "")
            if created_at:
                try:
                    formatted_date = datetime.fromisoformat(created_at).strftime("%B %d, %Y %I:%M %p")
                except ValueError:
                    formatted_date = created_at[:10]
            else:
                formatted_date = datetime.now().strftime('%Y-%m-%d')

            with st.expander(f"{saved_report.get('report_type', 'Report')} - {formatted_date}"):
                action_col1, action_col2 = st.columns(2)
                with action_col1:
                    if st.button("Load Into Editor", key=f"load_report_{index}", use_container_width=True):
                        st.session_state.report_type = saved_report.get("report_type", "Daily Report")
                        st.session_state.task_input = saved_report.get("task_input", "")
                        st.rerun()
                with action_col2:
                    can_delete = bool(saved_report.get("report_id"))
                    if st.button("Delete Report", key=f"delete_report_{index}", use_container_width=True, disabled=not can_delete):
                        try:
                            deleted = delete_saved_report(saved_report["report_id"])
                            if deleted:
                                st.session_state.saved_reports = [
                                    report for report in st.session_state.saved_reports
                                    if report.get("report_id") != saved_report.get("report_id")
                                ]
                                st.rerun()
                        except Exception:
                            st.error("Could not delete the saved report.")
                st.markdown(saved_report.get("content", ""))
    
    # Writing Guidelines
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="color: var(--text-muted); font-size: 0.7rem; font-weight: 600; 
                text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;">
        Writing Guidelines
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 16px; padding: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                <div style="width: 24px; height: 24px; border-radius: 6px; background: rgba(34, 197, 94, 0.15);
                            display: flex; align-items: center; justify-content: center;">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="3">
                        <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                </div>
                <span style="color: #22c55e; font-weight: 600; font-size: 0.9rem;">Best Practices</span>
            </div>
            <ul style="color: var(--text-secondary); font-size: 0.875rem; line-height: 2; padding-left: 1.25rem; margin: 0;">
                <li>Be specific about tasks completed</li>
                <li>Include names of collaborators</li>
                <li>Mention tools or systems used</li>
                <li>Note any challenges overcome</li>
                <li>Highlight measurable outcomes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 16px; padding: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                <div style="width: 24px; height: 24px; border-radius: 6px; background: rgba(239, 68, 68, 0.15);
                            display: flex; align-items: center; justify-content: center;">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="3">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                </div>
                <span style="color: #ef4444; font-weight: 600; font-size: 0.9rem;">Avoid These</span>
            </div>
            <ul style="color: var(--text-secondary); font-size: 0.875rem; line-height: 2; padding-left: 1.25rem; margin: 0;">
                <li>Vague descriptions ("did work")</li>
                <li>Including personal activities</li>
                <li>Forgetting to mention outcomes</li>
                <li>Submitting without proofreading</li>
                <li>Using informal language</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
