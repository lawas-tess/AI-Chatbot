# InTurn.AI — Smart Internship Assistant

An AI-powered internship tracking assistant for university students.  
Includes three tools: **InternTrack** (hours tracking), **MentorBridge** (workplace communication), and **Report Writer** (professional activity reports).

## Latest Updates

- InternTrack now supports signed hour updates from chat input:
	- `+8`, `+ 8 hours`, `-2`, `- 2 hrs`
- Hour updates are saved to backend config automatically.
- `Days Left` is calculated using your configured **Daily Hours**.
- Added AI disclaimer blocks in all AI sections.
- Added English-only input validation in backend routing.
- Added internship-scope guard response:
	- "I can only help with internship-related topics in InternTrack, MentorBridge, and ReportWriter."
- MentorBridge is now handled as single-turn (no prior chat history is sent).
- The backend now includes a local RAG layer over markdown knowledge files.
- The backend can also call tools during generation for an agentic reasoning loop.
- Added prompt-injection defenses that refuse obvious prompt override attempts.
- Chat UI now uses Messenger-style alignment:
	- User messages on the right (orange avatar)
	- Assistant messages on the left (red avatar)
	- Bubble width auto-adjusts based on content.

## Tech Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Frontend | Streamlit                         |
| Backend  | FastAPI + Uvicorn                 |
| Database | MongoDB (local or Atlas)          |
| AI       | OpenAI GPT-4o + local RAG + tools + Langfuse tracing |

---

## Prerequisites

- Python 3.11+
- MongoDB running locally on `localhost:27017` **or** a MongoDB Atlas cluster
- An OpenAI API key

For Langfuse tracing, add these environment variables to your `.env` file:

```env
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com
LANGFUSE_TRACING_ENABLED=true
LANGFUSE_TRACING_ENVIRONMENT=development
LANGFUSE_RELEASE=ai-chatbot
```

The app still runs without them, but Langfuse tracing stays disabled until the keys are set.

### Langfuse prompt management

This app now fetches its system prompts from Langfuse by prompt name and label. The prompt names used by the backend are:

- `interntrack-system-prompt`
- `mentorbridge-system-prompt`
- `report-writer-system-prompt`
- `chatbot-security-prompt`

The app loads the `production` label by default and records the prompt name, label, and version in each Langfuse trace.
If a prompt does not exist yet, the backend can seed it automatically from the current fallback text the first time it runs.

If you update a prompt in Langfuse, the app will pick up the new version the next time it fetches that prompt.

---

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd AI-Chatbot
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### 4. Create the `.env` file

Create a `.env` file in the **project root** (same level as this README):

```
OPENAI_API_KEY=your_openai_api_key_here
API_BASE_URL=http://your_railway_url
```

`API_BASE_URL` is optional and defaults to `http://localhost:8001`.


## Running the App

You need **two terminals** running at the same time.

### Terminal 1 — Start the backend

```bash
cd backend
uvicorn main:app --reload --port 8001
```

Backend runs at: `http://localhost:8001`  
API docs available at: `http://localhost:8001/docs`

### Terminal 2 — Start the frontend

```bash
cd frontend
streamlit run app.py
```

Frontend runs at: `http://localhost:8501`

---

## InternTrack Input Behavior

InternTrack accepts quick chat commands for hours updates.

- Add hours: `+8 today`
- Subtract hours: `-2 correction`

Rules:

- Hours are clamped between `0` and `Total Required Hours`.
- `Days Left` updates using `ceil(remaining / daily_hours)`.
- `Daily Hours` comes from the Configuration panel.

---

## Language and Scope Rules

- The backend accepts **English-only** user input.
- Non-English input receives this response:
	- `Please write your message in English only.`
- Programming/coding queries are out of scope and receive this response:
	- `I can only help with internship-related topics in InternTrack, MentorBridge, and ReportWriter.`

---

## MentorBridge Behavior

- MentorBridge runs in **single-turn mode**.
- Previous MentorBridge messages are not carried into new prompts.
- This keeps each workplace-message draft focused on the latest situation only.

---

## MongoDB Collections

The app uses a database named `interntrack` with these collections:

| Collection | Purpose                              |
|------------|--------------------------------------|
| `hours`    | Logged internship hours              |
| `tasks`    | Task entries                         |
| `chat`     | All chat messages (all three tools)  |
| `config`   | Saved InternTrack configuration      |
| `reports`  | Generated Report Writer reports      |

---

## Project Structure

```
AI-Chatbot/
├── backend/
│   ├── main.py          # FastAPI app and routes
│   ├── ai_router.py     # AI prompt routing (InternTrack / MentorBridge / Report Writer)
│   ├── database.py      # MongoDB connection and collections
│   └── tracker.py       # Hours logging logic
│   └── knowledge_base/  # Markdown files used by the retriever
├── frontend/
│   ├── app.py           # Streamlit UI
│   └── styles.py        # CSS styles
├── .env                 # API keys (never commit this)
├── .gitignore
└── README.md
```

