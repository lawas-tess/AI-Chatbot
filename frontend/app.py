import streamlit as st
import requests

API = "http://localhost:8001"

st.set_page_config(layout="wide", page_title="InternAssist AI")

# ── SIDEBAR NAV ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("InternAssist")
    st.caption("CSIT349-G01")
    st.divider()

    if "page" not in st.session_state:
        st.session_state.page = "InternTrack"

    if st.button("InternTrack", use_container_width=True):
        st.session_state.page = "InternTrack"

    if st.button("MentorBridge", use_container_width=True):
        st.session_state.page = "MentorBridge"

# ── INTERNTRACK PAGE ──────────────────────────────────────────────────────────
if st.session_state.page == "InternTrack":

    with st.sidebar:
        st.divider()
        st.header("Setup")
        total_hours = st.number_input("Total Required Hours", value=500)
        current_hours = st.number_input("Current Hours Logged", value=0)
        daily_hours = st.number_input("Daily Working Hours", value=8)
        start_date = st.date_input("Internship Start Date")
        country = st.selectbox(
            "Company Country",
            ["Singapore", "Philippines", "USA", "Japan"]
        )
        days = st.multiselect(
            "Working Days",
            ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            default=["Mon", "Tue", "Wed", "Thu", "Fri"]
        )
        st.button("Start Tracking")
        percent = (current_hours / total_hours) * 100 if total_hours else 0
        st.metric("Progress", f"{percent:.2f}%")

    st.title("InternTrack")
    st.caption("Log your hours, track your progress, and stay on top of your internship.")
    st.divider()

    if "interntrack_messages" not in st.session_state:
        st.session_state.interntrack_messages = []

    if not st.session_state.interntrack_messages:
        st.write("**Try one of these to get started:**")
        it_suggestions = [
            "I need to start tracking my internship. Can you help me set up?",
            "+8 today. I completed a client presentation and wrote a progress report.",
            "How many hours do I have left and when will I finish?",
            "Can you give me a weekly report of my progress?",
        ]
        for i, s in enumerate(it_suggestions):
            if st.button(s, key=f"it_btn_{i}", use_container_width=True):
                st.session_state.interntrack_messages.append({"role": "user", "content": s})
                st.rerun()

    for m in st.session_state.interntrack_messages:
        st.chat_message(m["role"]).write(m["content"])

    if user_input := st.chat_input("Ask something about your internship hours...", key="interntrack_input"):
        st.session_state.interntrack_messages.append({"role": "user", "content": user_input})
        try:
            res = requests.post(f"{API}/chat", json={"message": user_input})
            reply = res.json()["reply"]
        except Exception:
            reply = "_(Could not connect to backend. Make sure the backend is running.)_"
        st.session_state.interntrack_messages.append({"role": "assistant", "content": reply})
        st.rerun()

# ── MENTORBRIDGE PAGE ─────────────────────────────────────────────────────────
elif st.session_state.page == "MentorBridge":

    st.title("MentorBridge")
    st.caption("Find the right words when approaching your supervisor or mentor.")
    st.divider()

    if "mentorbridge_messages" not in st.session_state:
        st.session_state.mentorbridge_messages = []

    if not st.session_state.mentorbridge_messages:
        st.write("**Try one of these to get started:**")
        mb_suggestions = [
            "What do I say to Sir John to tell him I didn't fully understand the task he gave me?",
            "What do I say to Ma'am Sarah if I need to ask permission to leave early this Friday?",
            "What do I say to Sir Mark to admit that I made a mistake on the report he assigned me?",
            "What do I say to my supervisor if I feel like the workload is already too much for me?",
        ]
        for i, s in enumerate(mb_suggestions):
            if st.button(s, key=f"mb_btn_{i}", use_container_width=True):
                st.session_state.mentorbridge_messages.append({"role": "user", "content": s})
                st.rerun()

    for m in st.session_state.mentorbridge_messages:
        st.chat_message(m["role"]).write(m["content"])

    if user_input := st.chat_input("Describe your workplace situation...", key="mentorbridge_input"):
        st.session_state.mentorbridge_messages.append({"role": "user", "content": user_input})
        try:
            res = requests.post(f"{API}/chat", json={"message": user_input})
            reply = res.json()["reply"]
        except Exception:
            reply = "_(Could not connect to backend. Make sure the backend is running.)_"
        st.session_state.mentorbridge_messages.append({"role": "assistant", "content": reply})
        st.rerun()