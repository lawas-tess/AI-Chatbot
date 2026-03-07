import streamlit as st
import requests

API = "http://localhost:8001"

st.set_page_config(layout="wide")

st.title("InternTrack AI")

# Sidebar setup
with st.sidebar:

    st.header("Setup")

    total_hours = st.number_input("Total Required Hours", value=500)

    current_hours = st.number_input("Current Hours Logged", value=0)

    daily_hours = st.number_input("Daily Working Hours", value=8)

    start_date = st.date_input("Internship Start Date")

    country = st.selectbox(
        "Company Country",
        ["Singapore","Philippines","USA","Japan"]
    )

    days = st.multiselect(
        "Working Days",
        ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
        default=["Mon","Tue","Wed","Thu","Fri"]
    )

    start_tracking = st.button("Start Tracking")

# Progress box
percent = (current_hours / total_hours) * 100 if total_hours else 0

st.sidebar.metric("Progress", f"{percent:.2f}%")

# Chat area
st.subheader("InternTrack AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

user_input = st.chat_input("Ask something...")

if user_input:

    st.session_state.messages.append(
        {"role":"user","content":user_input}
    )

    res = requests.post(
        f"{API}/chat",
        json={"message": user_input}
    )

    reply = res.json()["reply"]

    st.session_state.messages.append(
        {"role":"assistant","content":reply}
    )

    st.rerun()