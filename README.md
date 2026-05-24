# 🎯 AI Interview Coach

A Streamlit-powered interview preparation tool that uses OpenAI's GPT-4o to simulate realistic job interviews across **any role, industry, or seniority level**. Get grilled by an AI panel, then receive structured, actionable feedback — no scheduling, no awkward handshakes.

---

## ✨ Features

- **Position-agnostic** — works for any job title (Data Scientist, Program Manager, DevOps Engineer, you name it)
- **Fully configurable role context** — set company, industry, seniority level, and interview style
- **Paste-in Job Description** — optional JD field so the AI targets questions to the actual role requirements
- **Multiple interview styles** — Behavioral (STAR), Technical Deep-Dive, Case Study, Culture Fit, or Mixed
- **Adjustable question count** — slider from 3–10 questions per session
- **Streaming responses** — real-time AI replies for a natural conversational feel
- **Structured feedback** — scored out of 10 with Strengths, Areas for Improvement, Hire Recommendation, and Top Tip
- **Downloadable feedback** — export results as `.txt` for post-interview reflection
- **Session state management** — clean multi-stage flow (Setup → Interview → Feedback → Restart)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend / UI | [Streamlit](https://streamlit.io/) |
| LLM Backend | [OpenAI GPT-4o](https://platform.openai.com/) via `openai` Python SDK |
| State Management | Streamlit `st.session_state` |
| Deployment | Streamlit Community Cloud / self-hosted |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- An OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# Install dependencies
pip install streamlit openai
```

### Configure API Key

Create a `.streamlit/secrets.toml` file in the project root:

```toml
OPENAI_API_KEY = "sk-..."
```

> ⚠️ **Never commit your API key.** Add `.streamlit/secrets.toml` to your `.gitignore`.

### Run the App

```bash
streamlit run interview_tool.py
```

The app will open at `http://localhost:8501`.

---

## 📂 Project Structure

```
.
├── interview_tool.py          # Main application
├── .streamlit/
│   └── secrets.toml           # API keys (gitignored)
├── requirements.txt           # Python dependencies
└── README.md
```

### `requirements.txt`

```
streamlit>=1.35.0
openai>=1.30.0
```

---

## 🗺️ App Flow

```
[Setup Stage]
    ├── Candidate: Name, Experience, Skills
    └── Role: Position (free text), Company, Industry, Level, Interview Style, JD (optional)
            │
            ▼
[Interview Stage]
    ├── AI interviewer greets candidate and asks questions one at a time
    ├── Streaming responses via GPT-4o
    └── Progress bar tracks question count (configurable 3–10)
            │
            ▼
[Feedback Stage]
    ├── Structured score out of 10
    ├── Strengths / Areas for Improvement / Hire Recommendation
    ├── Single top tip for next interview
    └── Download feedback as .txt
```

---

## ⚙️ Configuration Options

| Field | Type | Description |
|---|---|---|
| Full Name | Text input | Candidate name used in prompts |
| Seniority Level | Dropdown | Intern → Executive |
| Job Title / Position | Free text | Any role — no dropdown limits |
| Company | Free text | Target company for context |
| Industry / Domain | Free text | e.g., Defense, FinTech, Healthcare |
| Interview Style | Dropdown | Behavioral, Technical, Case Study, Culture Fit, Mixed |
| Job Description | Text area | Optional JD paste-in (up to 1,500 chars) |
| Question Count | Slider | 3–10 questions per session |

---

## 🐛 Changelog

### v2.0.0 — Position-Agnostic Refactor

**Bug Fixes**
- Fixed broken `from` import statement (incomplete import in original)
- Fixed duplicate column variable `col2, col2` → corrected to `col1, col2`
- Fixed undefined `col3` reference causing `NameError` at runtime
- Fixed incorrect OpenAI model name `"gpt-3o"` → `"gpt-4o"`
- Fixed `choices[1]` index error on feedback response → `choices[0]`
- Removed dependency on `streamlit_js_eval` (not installed); replaced with native `st.rerun()`

**Enhancements**
- Replaced hardcoded position/company dropdowns with free-text inputs — any role is now supported
- Added Industry/Domain field for richer AI context
- Added Interview Style selector (Behavioral, Technical, Case Study, Culture Fit, Mixed)
- Added optional Job Description text area — JD is injected into the system prompt for targeted questions
- Added adjustable question count slider (3–10)
- Enriched system prompt to enforce single-question-per-turn behavior and role-specific framing
- Structured feedback format: score, strengths, improvements, hire recommendation, top tip
- Added feedback download as `.txt`
- Added required-field validation before interview start
- Added progress bar during interview
- Applied custom dark-mode CSS theme with Google Fonts

---

## 🔮 Roadmap / Future Improvements

- [ ] Base44 Agent Builder integration for enhanced workflow automation
- [ ] Support for Claude API (Anthropic) as an alternative LLM backend
- [ ] Voice input / text-to-speech for a more realistic interview feel
- [ ] Resume / CV upload (PDF) to auto-populate candidate profile
- [ ] Interview history persistence (database or file storage)
- [ ] Multi-round interview simulation (phone screen → technical → final panel)
- [ ] Export feedback to PDF or DOCX
- [ ] Admin dashboard for tracking sessions and scores over time

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

[MIT](LICENSE)

---

> Built with Streamlit + OpenAI GPT-4o. Because practicing interviews at 11pm is better than bombing them at 9am.
