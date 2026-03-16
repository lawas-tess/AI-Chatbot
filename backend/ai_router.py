import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from database import chat_collection, config_collection

try:
    import holidays as hol
    _HOLIDAYS_AVAILABLE = True
except ImportError:
    _HOLIDAYS_AVAILABLE = False

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ── SYSTEM PROMPTS ────────────────────────────────────────────────────────────

INTERNTRACK_PROMPT = """
You are InternTrack AI, a friendly and encouraging internship hours 
tracking assistant designed for university students completing mandatory 
internship programs.

ROLE:
Help students log their daily internship hours, calculate their progress,
log tasks completed, and estimate when they will complete their required hours.

ON START:
Ask the student for:
1. Their total required internship hours (e.g., 300, 500, 600)
2. Their internship start date
3. Their daily working hours (default: 8 hrs/day)
4. Their internship company's country (for public holidays)
5. Their current logged hours (if they are mid-internship)

TRACKING RULES:
- Always maintain a running total of hours logged and tasks completed
- When the user says "+8 today" or "I worked 6 hours today", update the total
  and ask for task details
- After the user provides task details, store and summarize them for the day
- Always calculate: hours remaining, % completed, estimated workdays left,
  estimated end date
- Account for weekends (Mon-Fri only) and public holidays by country
- Round percentage to 1 decimal place

OUTPUT FORMAT:
- A short encouraging message
- Progress breakdown: Total Goal, Hours Logged, Remaining, % Completed
- Tasks completed today, workdays remaining, estimated end date
- If requested, provide daily/weekly/monthly report with total hours
  and task summary

SAFETY RULES:
- Do not answer questions unrelated to internship tracking
- Do not provide academic, legal, or medical advice
- Do not ask for or store sensitive personal information
- If user seems stressed, respond with encouragement and suggest
  speaking to their school coordinator

TONE:
Be friendly, concise, and motivating.
"""

MENTORBRIDGE_PROMPT = """
You are MentorBridge, a professional workplace communication coach 
designed specifically for university interns.

ROLE:
Help interns navigate real workplace situations by providing them with 
practical opening lines, suggested scripts, and phrasing they can actually 
use when approaching people of higher rank or authority during their internship.

You also help students fix, improve, or correct messages and emails 
they want to send to their supervisors or school coordinators.

RESPONSE RULES:
- Always restate the situation in one sentence to confirm understanding
- Provide a clear opening line or script the student can use word-for-word
- Offer 2 variations: one formal, one semi-formal
- Briefly explain why the suggested approach works professionally
- End with one practical follow-up tip
- If the message contains a typo or mistake, fix it and return the corrected
  professional version
- If the student asks for steps on how to handle a workplace situation,
  provide clear numbered steps
- If the situation involves potential HR or legal issues, advise the
  student to speak with their school coordinator

OUTPUT FORMAT:
Situation: (1-sentence restatement)

Formal Version:
"(exact opening line or corrected message)"

Semi-Formal Version:
"(exact opening line or corrected message)"

Why this works: (brief explanation)

What to do next: (one practical follow-up tip)

SAFETY RULES:
- Only answer questions related to workplace communication
- Do not provide legal, medical, or academic advice
- Be warm, practical, and direct like a knowledgeable older peer
"""

REPORT_PROMPT = """
You are a professional report writer assistant for university interns.

The student will give you a list of tasks they did during the day in any 
format — messy, short, casual, broken English, or incomplete sentences.

Your job is to turn those tasks into a clean, professional activity report.

RULES:
- Always write in a clear, professional tone.
- Expand short task descriptions into full, proper sentences without adding fake details.
- Group similar tasks together.
- DO NOT use "fluff" or "corporate speak" (e.g., avoid "enhancing productivity," "facilitating a working environment," or "maintaining an efficient workflow").
- Keep the summary literal. Describe exactly WHAT was done, not the "higher purpose" or "value" of the task.
- If the message contains "Daily Report" generate a Daily Activity Report.
- If the message contains "Weekly Report" generate a Weekly Activity Report.
- If the message contains "Monthly Report" generate a Monthly Activity Report.

OUTPUT FORMAT:

For DAILY:
---
DAILY ACTIVITY REPORT
Date: (use today's date if not provided)

Tasks Accomplished:
1. (expanded professional description of task)
2. (expanded professional description of task)

Summary:
(A 1-2 sentence literal summary. For example: "Today I completed [Task A] and researched [Topic B].")
---

... (Keep Weekly/Monthly formats as they were) ...

TONE:
Be professional and direct. Avoid flowery language, buzzwords, or exaggerated descriptions of simple tasks. Think "Technical Documentation" rather than "Marketing Brochure."
"""

# ── KEYWORD DETECTION ─────────────────────────────────────────────────────────

MENTORBRIDGE_KEYWORDS = [
    "what do i say", "how do i tell", "how do i ask",
    "supervisor", "mentor", "co-worker", "colleague",
    "leave early", "recommendation letter",
    "workload", "approach", "communicate", "apology",
    "apologize", "permission", "talk to", "tell my boss",
    "tell my supervisor", "say to my", "say to sir",
    "say to maam", "say to ma am",
    "wrong id", "wrong number", "correction", "amend",
    "submitted wrong", "i made a mistake", "typo",
    "request assistance", "i am writing to",
    "check this message", "check this messag",
    "fix my message", "fix this message",
    "can you check", "i want to know what steps",
    "what steps do i take", "how do i handle",
    "how do i approach", "i need help saying",
    "absent", "late submission", "i will be absent",
    "going to be absent", "cannot attend",
    "respectfully request", "writing to inform",
    "good morning sir", "good afternoon sir",
    "good evening sir", "good day sir",
    "good morning maam", "good afternoon maam",
    "good evening maam", "good day maam",
]

REPORT_KEYWORDS = [
    "daily report", "weekly report", "monthly report",
    "activity report", "tasks today", "tasks this week",
    "tasks this month", "write my report", "make my report",
    "generate report", "write a report", "create a report",
    "report for today", "report for this week",
    "report for this month",
    "please write a daily",
    "please write a weekly",
    "please write a monthly",
    "write a daily",
    "write a weekly",
    "write a monthly",
]

# ── ROUTE DETECTION ───────────────────────────────────────────────────────────

def detect_route(message: str) -> str:
    message_lower = message.lower()

    # MentorBridge FIRST — takes priority over report
    if any(k in message_lower for k in MENTORBRIDGE_KEYWORDS):
        return "mentorbridge"
    elif any(k in message_lower for k in REPORT_KEYWORDS):
        return "report"
    else:
        return "interntrack"

# ── MAIN CHAT FUNCTION ────────────────────────────────────────────────────────

def _get_country_holidays(country):
    if not _HOLIDAYS_AVAILABLE:
        return ""
    _country_map = {"Philippines": "PH", "Singapore": "SG", "USA": "US", "Japan": "JP"}
    code = _country_map.get(country)
    if not code:
        return ""
    try:
        h = hol.country_holidays(code, years=datetime.now().year)
        return "\n".join(
            f"  - {d.strftime('%B %d, %Y')}: {name}" for d, name in sorted(h.items())
        )
    except Exception:
        return ""


def _build_interntrack_prompt():
    config = config_collection.find_one({}, {"_id": 0})
    if not config:
        return INTERNTRACK_PROMPT

    country = config.get("country", "")
    holidays_text = _get_country_holidays(country)

    config_section = f"""

STUDENT PROFILE (already configured — do NOT ask for this information again):
- Total Required Hours: {config.get('total_hours', 'Not set')}
- Current Logged Hours: {config.get('current_hours', 0)}
- Daily Working Hours: {config.get('daily_hours', 8)} hrs/day
- Internship Start Date: {config.get('start_date', 'Not set')}
- Country: {country or 'Not set'}
- Working Days: {', '.join(config.get('working_days', ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']))}
"""

    if holidays_text:
        config_section += f"""
{country} Public Holidays {datetime.now().year} (do NOT count these as working days):
{holidays_text}
"""

    return INTERNTRACK_PROMPT + config_section


def chat_ai(message, history=None):

    route = detect_route(message)

    if route == "report":
        system = REPORT_PROMPT
    elif route == "mentorbridge":
        system = MENTORBRIDGE_PROMPT
    else:
        system = _build_interntrack_prompt()

    messages = [{"role": "system", "content": system}]

    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        reply = response.choices[0].message.content

        chat_collection.insert_one({
            "user": message,
            "assistant": reply,
            "route": route,
            "timestamp": datetime.utcnow()
        })

        return {"reply": reply}

    except Exception as e:
        return {"reply": f"Error connecting to AI: {str(e)}"}