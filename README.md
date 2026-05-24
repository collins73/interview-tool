# 🎙️ AI Interview Tool

An AI-powered mock interview simulator built with **Streamlit** and **OpenAI GPT-4o**. Practice job interviews for top tech and data roles, get real-time conversational feedback from a simulated HR executive, and receive a scored performance review — all in your browser.

> *Because practicing in the mirror only tells you so much.*

---

## 🚀 Features

- **Personalized Interview Setup** — Enter your name, experience, and skills before the session begins
- **Role & Company Targeting** — Select your target level (Junior / Mid-level / Senior), position, and company
- **AI-Driven HR Interviewer** — GPT-4o plays the role of an HR executive tailored to your profile
- **5-Round Conversation Flow** — Structured interview with up to 5 exchanges to keep sessions focused
- **Automated Feedback & Scoring** — After the interview, receive a 1–10 score and detailed performance feedback
- **Session State Management** — Clean multi-stage flow: Setup → Interview → Feedback → Restart

---

## 🖥️ Supported Roles & Companies

| Positions | Companies |
|-----------|-----------|
| Data Scientist | Amazon |
| Data Engineer | Meta |
| ML Engineer | Udemy |
| BI Analyst | LinkedIn |
| Financial Analyst | Spotify |
| | Nestle |
| | 365 Company |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend / UI | [Streamlit](https://streamlit.io/) |
| AI Engine | [OpenAI GPT-4o](https://platform.openai.com/docs/) |
| Language | Python 3.9+ |
| State Management | Streamlit Session State |

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/collins73/interview-tool.git
cd interview-tool
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install streamlit openai
```

### 4. Configure Your OpenAI API Key

Create a Streamlit secrets file:

```bash
mkdir -p .streamlit
touch .streamlit/secrets.toml
```

Add your key to `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "sk-your-openai-api-key-here"
```

> ⚠️ **Never commit your API key to version control.** The `.gitignore` in this repo already excludes `.streamlit/secrets.toml`.

---

## ▶️ Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 🗺️ How It Works

```
1. Setup Screen
   └─ Enter name, experience, skills
   └─ Select level, position, and target company
   └─ Click "Start Interview"

2. Interview Screen
   └─ AI HR Executive introduces the session
   └─ You respond (up to 5 exchanges, 1000 chars each)
   └─ GPT-4o maintains context throughout

3. Feedback Screen
   └─ Click "Get Feedback"
   └─ Receive Overall Score (1–10) + detailed feedback
   └─ Restart anytime for another round
```

---

## 📁 Project Structure

```
interview-tool/
│
├── app.py              # Main Streamlit application
├── example1.py         # Example / prototype script
├── .gitignore          # Excludes secrets and env files
└── README.md           # You are here 📍
```

---

## 🔐 Security Notes

- API keys are loaded from Streamlit's secrets management — never hardcoded
- The `.gitignore` excludes `secrets.toml`, virtual environments, and compiled Python files
- No user data is stored or persisted beyond the active session

---

## 🔮 Roadmap / Future Enhancements

- [ ] Add support for technical / coding interview rounds
- [ ] Expand company and role library
- [ ] Export interview transcript as PDF
- [ ] Voice input/output via Whisper + TTS APIs
- [ ] Deploy to Streamlit Community Cloud with one-click setup
- [ ] User authentication and session history

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## 📄 License

This project is open source. See [LICENSE](LICENSE) for details.

---

## 👤 Author

**Demayne Collins**
- GitHub: [@collins73](https://github.com/collins73)

---

*Built to help job seekers practice smarter — because showing up unprepared is so last century.* 💼# interview-tool
