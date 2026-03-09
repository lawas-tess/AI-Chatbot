import streamlit as st
import requests

API = "http://localhost:8001"

# Helper function to send message and get AI response
def send_message(user_input, message_list):
    """Send a message to the API and return the AI response"""
    message_list.append({"role": "user", "content": user_input})
    try:
        history = message_list[:-1]  # All messages except the one we just added
        res = requests.post(
            f"{API}/chat",
            json={"message": user_input, "history": history},
            timeout=30
        )
        res.raise_for_status()
        reply = res.json()["reply"]
    except requests.exceptions.Timeout:
        reply = "⚠️ Request timed out. The AI is taking too long to respond."
    except requests.exceptions.ConnectionError:
        reply = "⚠️ Could not connect to backend. Make sure it's running on port 8001."
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"
    message_list.append({"role": "assistant", "content": reply})
    return reply

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

    if st.button("Report Writer", use_container_width=True):
        st.session_state.page = "Report Writer"

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
                with st.spinner("Thinking..."):
                    send_message(s, st.session_state.interntrack_messages)
                st.rerun()

    for m in st.session_state.interntrack_messages:
        st.chat_message(m["role"]).write(m["content"])

    if user_input := st.chat_input("Ask something about your internship hours...", key="interntrack_input"):
        with st.spinner("Thinking..."):
            send_message(user_input, st.session_state.interntrack_messages)
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
            "What do I say to Ma'am Sarah if I need to ask permission to ask permission to leave early this Friday?",
            "What do I say to Sir Mark to admit that I made a mistake on the report he assigned me?",
            "What do I say to my supervisor if I feel like the workload is already too much for me?",
        ]
        for i, s in enumerate(mb_suggestions):
            if st.button(s, key=f"mb_btn_{i}", use_container_width=True):
                with st.spinner("Thinking..."):
                    send_message(s, st.session_state.mentorbridge_messages)
                st.rerun()

    for m in st.session_state.mentorbridge_messages:
        st.chat_message(m["role"]).write(m["content"])

    if user_input := st.chat_input("Describe your workplace situation...", key="mentorbridge_input"):
        with st.spinner("Thinking..."):
            send_message(user_input, st.session_state.mentorbridge_messages)
        st.rerun()

# ── REPORT WRITER PAGE ────────────────────────────────────────────────────────
elif st.session_state.page == "Report Writer":

    st.title("Report Activity Writer")
    st.caption("Input your tasks for the day and the AI will generate a professional report.")
    st.divider()

    report_type = st.selectbox(
        "Report Type",
        ["Daily Report", "Weekly Report", "Monthly Report"],
        key="report_type"
    )

    task_input = st.text_area(
        "Enter your tasks (one per line or just type naturally)",
        placeholder="""Example:
-Include what month if Monthly Report.
- printed documents for sir john
- attended morning meeting
- updated excel spreadsheet for inventory
- got coffee for the team
- filed papers in cabinet""",
        height=200,
        key="task_input"
    )

    if st.button("Generate Report", use_container_width=True, key="generate_report"):
        if task_input.strip() == "":
            st.warning("Please enter your tasks first.")
        else:
            message = f"generate report. Please write a {report_type} for these tasks:\n{task_input}"
            with st.spinner("Generating your report..."):
                try:
                    res = requests.post(
                        f"{API}/chat",
                        json={"message": message},
                        timeout=30
                    )
                    res.raise_for_status()
                    report_output = res.json()["reply"]
                    st.divider()
                    st.subheader("Generated Report")
                    st.markdown(report_output)
                    st.divider()
                    st.download_button(
                        label="Download Report as .txt",
                        data=report_output,
                        file_name=f"{report_type.replace(' ', '_')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                except requests.exceptions.Timeout:
                    st.error("⚠️ Request timed out. The AI is taking too long to respond.")
                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Could not connect to backend. Make sure it's running on port 8001.")
                except Exception as e:
                    st.error(f"⚠️ Error: {str(e)}")