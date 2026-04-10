import os
import re
from datetime import datetime, date, timedelta
from dotenv import load_dotenv
from openai import OpenAI
from database import chat_collection, config_collection

try:
    from langdetect import detect_langs, DetectorFactory
    DetectorFactory.seed = 0
    _LANGDETECT_AVAILABLE = True
except ImportError:
    _LANGDETECT_AVAILABLE = False

try:
    import holidays as hol
    _HOLIDAYS_AVAILABLE = True
except ImportError:
    _HOLIDAYS_AVAILABLE = False

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Daily usage limits
PER_ROUTE_DAILY_LIMIT = 10
GLOBAL_DAILY_LIMIT = 30

# ── SYSTEM PROMPTS ────────────────────────────────────────────────────────────

INTERNTRACK_PROMPT = """
You are InternTrack AI, a friendly and encouraging internship hours 
tracking assistant designed for university students completing mandatory 
internship programs.

ROLE:
Help students log their daily internship hours, calculate their progress,
log tasks completed, and show when they will complete their required hours.

ON START:
ONLY ask for setup details if NO STUDENT PROFILE is provided at the bottom 
of this prompt. If a student profile IS provided, skip setup entirely and 
immediately answer the student's question using the provided data.

If no profile exists, ask the student for:
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
- ALWAYS use the pre-calculated values from the student profile below.
  DO NOT recalculate total hours, remaining hours, or estimated end date 
  on your own. These are already computed accurately in Python.
- Round percentage to 1 decimal place

OUTPUT FORMAT:
Always structure your response exactly as follows when showing progress:

**Progress Breakdown**
- Total Goal: X hours
- Hours Logged (as of today): X hours
- Remaining Hours: X hours

---

**Percentage Completed**
X.X%
*(short encouraging note about their progress)*

---

**Workdays Remaining**
X.X Days
*(Based on your X-hour daily schedule)*
- Full Workdays: X days
- Partial Day: X hours (X.X day)

---

**Estimated End Date**
*Day, Month DD, YYYY*
Use EXACTLY the pre-calculated estimated end date from the student profile.
DO NOT compute or guess this yourself.

---

**Timeline Considerations:**
- Only list public holidays from the student profile that fall between 
  today's date and the pre-calculated estimated end date.
- DO NOT mention any holidays beyond the estimated end date.
- For each relevant holiday, note if an off-in-lieu day applies.
- If there are no holidays in range, write: 
  "No public holidays fall within your remaining internship period."

---

After the structured output, add a short encouraging message.

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
practical, ready-to-send message drafts they can actually use when 
approaching supervisors, mentors, or colleagues of higher authority.

You also help students fix, improve, or evaluate messages and emails 
they want to send to their supervisors or school coordinators.

════════════════════════════════════════════
FLOW A — GENERATE A MESSAGE (no pre-written message)
Use this flow when the student just describes their situation 
and needs a message written for them.
════════════════════════════════════════════

OUTPUT FORMAT FOR FLOW A:

**Situation:** (1-sentence restatement of what the student needs)

---

**The Polished Version (Ready to Send):**
"(single professional message the student can use word-for-word)"

---

**Why this works:**
(1-2 sentences explaining the professional reasoning behind the approach)

---

**What to do next:**
- (practical step 1)
- (practical step 2)

---

💡 **Mentor Tip:** (one practical career advice tip related to the situation.
Be specific and actionable. Example: "Always send leave requests at least 
3–5 working days in advance to give your supervisor time to plan.")

════════════════════════════════════════════
FLOW B — EVALUATE A MESSAGE (student has a pre-written message)
Use this flow when the student shares their own drafted message 
and wants it checked, scored, or improved.
════════════════════════════════════════════

OUTPUT FORMAT FOR FLOW B:

**Situation:** (1-sentence restatement of what the student is trying to communicate)

---

⭐ **Overall Rating:** X/10

**The Breakdown:**
- **Clarity:** X/10 — (brief reason)
- **Tone:** X/10 — (brief reason)
- **Formality:** X/10 — (brief reason)

---

**The Polished Version (Ready to Send):**
"(corrected or improved version of the student's message)"

---

**What to do next:**
- (practical step 1)
- (practical step 2)

---

💡 **Mentor Tip:** (one practical career advice tip specific to this situation.
Make it concrete and useful, not generic. Example: "Pro-Tip: When resending 
a corrected document, always briefly state what was changed so the recipient 
knows exactly what to look for.")

---

(Optional closing line: offer to help draft a follow-up message if relevant)

════════════════════════════════════════════
ADDITIONAL RULES:
════════════════════════════════════════════
- Always use --- separators between every section
- If the student asks for steps on how to handle a situation, 
  provide clear numbered steps before the polished message
- If the situation involves potential HR or legal issues, advise the
  student to speak with their school coordinator
- If the score is below 7, ask: "Would you like me to generate an 
  updated version you can send right away?"
- If the score is 7 or above, confirm it is appropriate and provide 
  the polished version with minor improvements if needed

SAFETY RULES:
- Only answer questions related to workplace communication
- Do not provide legal, medical, or academic advice
- Be warm, practical, and direct — like a knowledgeable older peer

TONE:
Professional, encouraging, and direct. Never condescending.
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
- DO NOT use "fluff" or "corporate speak" (e.g., avoid "enhancing productivity," 
  "facilitating a working environment," or "maintaining an efficient workflow").
- Keep the summary literal. Describe exactly WHAT was done, not the "higher purpose" 
  or "value" of the task.
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
(A 1-2 sentence literal summary.)
---

TONE:
Be professional and direct. Avoid flowery language, buzzwords, or exaggerated 
descriptions of simple tasks. Think "Technical Documentation" not "Marketing Brochure."
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
    "day off", "leave on", "file a leave",
    "resend", "wrong file", "wrong attachment",
    "resubmit", "send again", "re-send",
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

PROGRAMMING_KEYWORDS = [
    "code", "coding", "programming", "python", "java", "javascript", "c++", "c#",
    "html", "css", "sql", "api", "backend", "frontend", "framework", "library",
    "loop", "loops", "array", "arrays", "list", "dictionary", "dict", "tuple",
    "function", "functions", "class", "classes", "object", "variable", "algorithm",
    "recursion", "syntax", "compile", "debug", "bug", "runtime", "stack trace"
]

NON_ENGLISH_KEYWORDS = [
    "hola", "gracias", "por favor", "adios", "como", "que", "porque", "donde",
    "cuando", "buenos dias", "buenas tardes", "buenas noches",
    "kamusta", "kumusta", "salamat", "magandang", "po", "opo", "paano", "bakit",
    "saan", "kailan", "bonjour", "merci", "au revoir", "xin chao", "cam on",
    "unsa", "kani", "kana", "nimo", "ako", "ikaw", "siya", "kami", "kamo",
    "ila", "dili", "wala", "naa", "mao", "ug", "kay", "para", "adto", "ani"
]

ENGLISH_COMMON_WORDS = {
    "the", "a", "an", "is", "are", "am", "was", "were", "be", "been", "being",
    "i", "you", "he", "she", "we", "they", "it", "my", "your", "our", "their",
    "to", "of", "in", "on", "for", "with", "from", "at", "by", "as", "and", "or",
    "do", "does", "did", "can", "could", "will", "would", "should", "may", "might",
    "how", "what", "when", "where", "why", "who", "which", "help", "please"
}

# ── ROUTE DETECTION ───────────────────────────────────────────────────────────

def detect_route(message: str) -> str:
    message_lower = message.lower()
    if any(k in message_lower for k in MENTORBRIDGE_KEYWORDS):
        return "mentorbridge"
    elif any(k in message_lower for k in REPORT_KEYWORDS):
        return "report"
    else:
        return "interntrack"


def _is_programming_query(message: str) -> bool:
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in PROGRAMMING_KEYWORDS)


def _is_english_only_message(message: str) -> bool:
    """Allow only English user input. Uses language detection when available."""
    message_lower = (message or "").lower().strip()
    if not message_lower:
        return True

    # Reject non-ASCII text to avoid handling non-English scripts.
    if re.search(r"[^\x00-\x7F]", message_lower):
        return False

    # Prefer robust language detection when the package is installed.
    if _LANGDETECT_AVAILABLE and len(message_lower) >= 20:
        try:
            candidates = detect_langs(message_lower)
            if not candidates:
                return False

            top_lang = candidates[0].lang
            top_prob = candidates[0].prob

            if top_lang == "en":
                return True

            # Strong non-English confidence means reject.
            if top_prob >= 0.90:
                return False
        except Exception:
            return False

    # Reject obvious non-English phrases written in ASCII.
    for keyword in NON_ENGLISH_KEYWORDS:
        if re.search(rf"\b{re.escape(keyword)}\b", message_lower):
            return False

    # Fallback lexical check for short/ambiguous ASCII text.
    tokens = re.findall(r"[a-zA-Z']+", message_lower)
    if not tokens:
        return True

    if len(tokens) <= 3:
        return True

    english_hits = sum(1 for t in tokens if t in ENGLISH_COMMON_WORDS)
    english_ratio = english_hits / len(tokens)
    return english_ratio >= 0.15

# ── DATE CALCULATION ──────────────────────────────────────────────────────────

_DAY_MAP = {
    "Mon": 0, "Tue": 1, "Wed": 2,
    "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6
}

_COUNTRY_MAP = {
    "Philippines": "PH",
    "Singapore": "SG",
    "USA": "US",
    "Japan": "JP"
}


def _get_holiday_dict(country: str) -> dict:
    """Return a dict of {date: holiday_name} for the given country (this year + next)."""
    if not _HOLIDAYS_AVAILABLE:
        return {}
    code = _COUNTRY_MAP.get(country)
    if not code:
        return {}
    try:
        today = datetime.now()
        h = hol.country_holidays(code, years=[today.year, today.year + 1])
        return {d: name for d, name in h.items()}
    except Exception:
        return {}


def _calculate_end_date(
    remaining_hours: int,
    daily_hours: int,
    working_days: list,
    holiday_dict: dict
) -> date:
    """
    Count forward from today, skipping non-working days and public holidays,
    until remaining_hours are consumed. Returns the estimated end date.
    """
    if daily_hours <= 0:
        daily_hours = 8

    working_day_numbers = {_DAY_MAP[d] for d in working_days if d in _DAY_MAP}
    hours_left = remaining_hours
    current = date.today()

    while hours_left > 0:
        if current.weekday() in working_day_numbers and current not in holiday_dict:
            hours_left -= daily_hours
        if hours_left > 0:
            current += timedelta(days=1)

    return current


def _format_holidays_in_range(
    holiday_dict: dict,
    end_date: date
) -> str:
    """Return a formatted string of holidays between today and end_date (inclusive)."""
    today = date.today()
    relevant = {
        d: name for d, name in holiday_dict.items()
        if today <= d <= end_date
    }
    if not relevant:
        return "  None — no public holidays fall within your remaining internship period."
    lines = []
    for d in sorted(relevant):
        lines.append(f"  - {d.strftime('%B %d, %Y')}: {relevant[d]}")
    return "\n".join(lines)


# ── PROMPT BUILDER ────────────────────────────────────────────────────────────

def _build_interntrack_prompt() -> str:
    config = config_collection.find_one({}, {"_id": 0})
    if not config:
        return INTERNTRACK_PROMPT

    total_hours   = int(config.get("total_hours", 500))
    current_hours = int(config.get("current_hours", 0))
    daily_hours   = int(config.get("daily_hours", 8))
    country       = config.get("country", "")
    working_days  = config.get("working_days", ["Mon", "Tue", "Wed", "Thu", "Fri"])

    remaining_hours = max(total_hours - current_hours, 0)
    full_days       = remaining_hours // daily_hours
    partial_hours   = remaining_hours % daily_hours
    partial_day     = round(partial_hours / daily_hours, 1) if partial_hours > 0 else 0
    total_days      = round(full_days + partial_day, 1)
    percentage      = round((current_hours / total_hours * 100), 1) if total_hours > 0 else 0.0

    # Python-calculated end date
    holiday_dict = _get_holiday_dict(country)
    end_date     = _calculate_end_date(remaining_hours, daily_hours, working_days, holiday_dict)
    end_date_str = end_date.strftime("%A, %B %d, %Y")

    # Holidays only within the OJT period
    holidays_in_range = _format_holidays_in_range(holiday_dict, end_date)

    config_section = f"""

================================================================================
CRITICAL INSTRUCTION — READ BEFORE RESPONDING:
- The student has ALREADY completed their setup. 
- DO NOT ask for total hours, current hours, start date, daily hours, 
  country, or working days. This information is already known.
- DO NOT recalculate the estimated end date. It has been pre-calculated 
  accurately in Python. Use it exactly as shown below.
- Respond immediately using the data provided in the student profile.
================================================================================

STUDENT PROFILE (pre-configured — use these values directly):
- Total Required Hours  : {total_hours} hours
- Hours Logged (today)  : {current_hours} hours
- Remaining Hours       : {remaining_hours} hours
- Percentage Completed  : {percentage}%
- Daily Working Hours   : {daily_hours} hrs/day
- Working Days          : {', '.join(working_days)}
- Country               : {country or 'Not set'}
- Internship Start Date : {config.get('start_date', 'Not set')}

PRE-CALCULATED PROGRESS (use these exactly — DO NOT recompute):
- Total Workdays Remaining : {total_days} days
- Full Workdays             : {full_days} days
- Partial Day              : {partial_hours} hours ({partial_day} day)
- Estimated End Date       : {end_date_str}

PUBLIC HOLIDAYS WITHIN OJT PERIOD (today → {end_date_str}):
{holidays_in_range}
(DO NOT mention any holidays outside this range.)
================================================================================
"""

    return INTERNTRACK_PROMPT + config_section


def _get_daily_usage_counts() -> dict:
    """Return today's usage counts for each route and globally (UTC day)."""
    now = datetime.utcnow()
    day_start = datetime(now.year, now.month, now.day)
    next_day = day_start + timedelta(days=1)

    day_filter = {"timestamp": {"$gte": day_start, "$lt": next_day}}

    total_count = chat_collection.count_documents(day_filter)
    route_counts = {
        "interntrack": chat_collection.count_documents({**day_filter, "route": "interntrack"}),
        "mentorbridge": chat_collection.count_documents({**day_filter, "route": "mentorbridge"}),
        "report": chat_collection.count_documents({**day_filter, "route": "report"})
    }

    return {
        "total": total_count,
        "routes": route_counts
    }


# ── MAIN CHAT FUNCTION ────────────────────────────────────────────────────────

def chat_ai(message, history=None):
    route = detect_route(message)

    if not _is_english_only_message(message):
        return {
            "reply": "Please write your message in English only."
        }

    if _is_programming_query(message):
        return {
            "reply": (
                "I can only help with internship-related topics in InternTrack, "
                "MentorBridge, and ReportWriter."
            )
        }

    # Keep MentorBridge single-turn to avoid carrying prior conversation context.
    if route == "mentorbridge":
        history = []

    usage = _get_daily_usage_counts()
    if usage["total"] >= GLOBAL_DAILY_LIMIT:
        return {
            "reply": (
                "Daily limit reached: 30/30 total messages used today across "
                "InternTrack, MentorBridge, and ReportWriter."
            )
        }

    route_usage = usage["routes"].get(route, 0)
    if route_usage >= PER_ROUTE_DAILY_LIMIT:
        route_label = {
            "interntrack": "InternTrack",
            "mentorbridge": "MentorBridge",
            "report": "ReportWriter"
        }.get(route, route)
        return {
            "reply": (
                f"Daily limit reached for {route_label}: "
                f"{PER_ROUTE_DAILY_LIMIT}/{PER_ROUTE_DAILY_LIMIT} messages used today."
            )
        }

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
            model="gpt-4o",
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