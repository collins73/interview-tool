import streamlit as st
from openai import OpenAI

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(page_title="AI Interview Coach", page_icon="🎯", layout="centered")

# ─────────────────────────────────────────────
# Custom CSS — sleek dark interview room vibes
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #0f1117;
        color: #e8e8e8;
    }
    h1, h2, h3 {
        font-family: 'DM Serif Display', serif;
        color: #f0f0f0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #1a73e8, #0d47a1);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2196f3, #1565c0);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(26, 115, 232, 0.4);
    }
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        background-color: #1e2130;
        color: #e8e8e8;
        border: 1px solid #2d3147;
        border-radius: 8px;
    }
    .stRadio > div {
        background-color: #1e2130;
        border-radius: 8px;
        padding: 0.5rem;
    }
    .info-box {
        background: linear-gradient(135deg, #1a1f35, #0d1829);
        border-left: 3px solid #1a73e8;
        padding: 1rem 1.5rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    .score-card {
        background: linear-gradient(135deg, #1a1f35, #0d1829);
        border: 1px solid #2d3147;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .step-badge {
        background: #1a73e8;
        color: white;
        border-radius: 20px;
        padding: 2px 12px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    div[data-testid="stChatMessage"] {
        background-color: #1e2130;
        border-radius: 12px;
        margin: 0.5rem 0;
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Session state initialization
# ─────────────────────────────────────────────
defaults = {
    "setup_complete": False,
    "user_message_count": 1,
    "feedback_shown": False,
    "chat_complete": False,
    "messages": [],
    "name": "",
    "experience": "",
    "skills": "",
    "level": "Mid-level",
    "position": "",
    "position_custom": False,
    "company": "",
    "industry": "",
    "job_description": "",
    "interview_style": "Behavioral",
    "question_count": 5,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ─────────────────────────────────────────────
# Callbacks
# ─────────────────────────────────────────────
def complete_setup():
    st.session_state.setup_complete = True

def show_feedback():
    st.session_state.feedback_shown = True

def restart():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# ─────────────────────────────────────────────
# STAGE 1 — Setup
# ─────────────────────────────────────────────
if not st.session_state.setup_complete:

    st.title("🎯 AI Interview Coach")
    st.markdown(
        '<div class="info-box">Answer up to <strong>5 questions</strong> from your virtual interviewer. '
        'Get scored and receive actionable feedback. '
        '<em>No awkward handshakes required.</em></div>',
        unsafe_allow_html=True
    )

    # ── Candidate Info ──────────────────────────
    st.markdown("### 👤 Candidate Profile")
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.session_state["name"] = st.text_input(
            "Full Name *",
            value=st.session_state["name"],
            placeholder="Jane Doe",
            max_chars=60
        )
    with col_b:
        st.session_state["level"] = st.selectbox(
            "Seniority Level *",
            ["Intern", "Junior", "Mid-level", "Senior", "Lead", "Principal", "Director", "Executive"],
            index=["Intern", "Junior", "Mid-level", "Senior", "Lead", "Principal", "Director", "Executive"]
                  .index(st.session_state["level"])
        )

    st.session_state["experience"] = st.text_area(
        "Relevant Experience *",
        value=st.session_state["experience"],
        placeholder="Briefly describe your work history and key accomplishments...",
        max_chars=500,
        height=100
    )
    st.session_state["skills"] = st.text_area(
        "Key Skills *",
        value=st.session_state["skills"],
        placeholder="e.g. Python, project management, stakeholder communication, cloud architecture...",
        max_chars=300,
        height=80
    )

    st.divider()

    # ── Role Info ────────────────────────────────
    st.markdown("### 🏢 Role Details")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.session_state["position"] = st.text_input(
            "Job Title / Position *",
            value=st.session_state["position"],
            placeholder="e.g. Program Manager, DevOps Engineer, UX Researcher..."
        )
    with col2:
        st.session_state["company"] = st.text_input(
            "Company / Organization",
            value=st.session_state["company"],
            placeholder="e.g. Lockheed Martin, Google, a stealth startup..."
        )

    col3, col4 = st.columns([1, 1])
    with col3:
        st.session_state["industry"] = st.text_input(
            "Industry / Domain",
            value=st.session_state["industry"],
            placeholder="e.g. Defense, FinTech, Healthcare, SaaS..."
        )
    with col4:
        st.session_state["interview_style"] = st.selectbox(
            "Interview Focus",
            ["Behavioral (STAR-based)", "Technical Deep-Dive", "Case Study / Problem Solving",
             "Culture Fit", "Mixed (Behavioral + Technical)"],
            index=0
        )

    st.session_state["job_description"] = st.text_area(
        "Job Description / Requirements (optional but recommended)",
        value=st.session_state["job_description"],
        placeholder="Paste the JD or key requirements here. The more context, the sharper the questions...",
        max_chars=1500,
        height=120
    )

    st.session_state["question_count"] = st.slider(
        "Number of Interview Questions",
        min_value=3, max_value=10, value=5,
        help="How many back-and-forth exchanges before feedback is generated"
    )

    st.divider()

    # ── Validation ────────────────────────────────
    required_filled = all([
        st.session_state["name"].strip(),
        st.session_state["experience"].strip(),
        st.session_state["skills"].strip(),
        st.session_state["position"].strip(),
    ])

    if not required_filled:
        st.warning("⚠️ Please fill in all required fields (*) before starting.")

    if st.button("🚀 Start Interview", on_click=complete_setup, disabled=not required_filled):
        st.write("Buckle up — the panel is ready for you.")

# ─────────────────────────────────────────────
# STAGE 2 — Interview
# ─────────────────────────────────────────────
if st.session_state.setup_complete and not st.session_state.feedback_shown and not st.session_state.chat_complete:

    company_display = f" at **{st.session_state['company']}**" if st.session_state["company"] else ""
    industry_display = f" ({st.session_state['industry']})" if st.session_state["industry"] else ""

    st.title("🎤 Interview in Progress")
    st.markdown(
        f'<div class="info-box">'
        f'Interviewing <strong>{st.session_state["name"]}</strong> for '
        f'<strong>{st.session_state["level"]} {st.session_state["position"]}</strong>'
        f'{company_display}{industry_display} &nbsp;|&nbsp; '
        f'Focus: <strong>{st.session_state["interview_style"]}</strong>'
        f'</div>',
        unsafe_allow_html=True
    )

    # Progress indicator
    max_exchanges = st.session_state["question_count"]
    current_q = min((st.session_state.user_message_count - 1) // 2 + 1, max_exchanges)
    progress_pct = min((st.session_state.user_message_count - 1) / (max_exchanges * 2), 1.0)
    st.progress(progress_pct, text=f"Question {current_q} of {max_exchanges}")

    # OpenAI client
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o"

    # Build system prompt — position-agnostic and rich with context
    if not st.session_state.messages:
        jd_section = (
            f"\n\nJob Description / Requirements provided:\n{st.session_state['job_description']}"
            if st.session_state["job_description"].strip()
            else ""
        )
        company_section = (
            f" at {st.session_state['company']}" if st.session_state["company"] else ""
        )
        industry_section = (
            f" in the {st.session_state['industry']} industry" if st.session_state["industry"] else ""
        )

        system_prompt = (
            f"You are a professional interviewer conducting a {st.session_state['interview_style']} interview "
            f"for the position of {st.session_state['level']} {st.session_state['position']}"
            f"{company_section}{industry_section}.\n\n"
            f"Candidate name: {st.session_state['name']}\n"
            f"Their experience: {st.session_state['experience']}\n"
            f"Their skills: {st.session_state['skills']}"
            f"{jd_section}\n\n"
            f"Instructions:\n"
            f"- Ask one focused question at a time. Do NOT ask multiple questions in a single turn.\n"
            f"- Tailor questions specifically to the role, industry, and seniority level provided.\n"
            f"- For '{st.session_state['interview_style']}', use the appropriate question format "
            f"(e.g., STAR prompts for behavioral, technical problems for technical deep-dives).\n"
            f"- Acknowledge the candidate's answer briefly before asking the next question (1-2 sentences max).\n"
            f"- Do NOT provide feedback, scores, or commentary during the interview — save that for the end.\n"
            f"- Keep a professional but approachable tone.\n"
            f"- Start by greeting {st.session_state['name']} and asking them to briefly introduce themselves."
        )

        st.session_state.messages = [{"role": "system", "content": system_prompt}]

        # Auto-trigger first greeting from interviewer
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=st.session_state.messages,
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Display message history (skip system prompt)
    else:
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    # Chat input
    max_user_turns = st.session_state["question_count"]
    if st.session_state.user_message_count <= max_user_turns:
        if prompt := st.chat_input(
            f"Your response ({st.session_state.user_message_count}/{max_user_turns})",
            max_chars=1200
        ):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Only generate next question if not on the last answer
            if st.session_state.user_message_count < max_user_turns:
                with st.chat_message("assistant"):
                    stream = client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        stream=True,
                    )
                    response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})

            st.session_state["user_message_count"] += 1

    if st.session_state.user_message_count > max_user_turns:
        st.session_state.chat_complete = True
        st.rerun()

# ─────────────────────────────────────────────
# STAGE 3 — Get Feedback button
# ─────────────────────────────────────────────
if st.session_state.chat_complete and not st.session_state.feedback_shown:
    st.success("✅ Interview complete! The panel has heard enough — time to find out if you impressed them.")
    if st.button("📊 Get My Feedback", on_click=show_feedback):
        st.write("Crunching the data... (The AI judge is putting on its monocle)")

# ─────────────────────────────────────────────
# STAGE 4 — Feedback
# ─────────────────────────────────────────────
if st.session_state.feedback_shown:

    st.title("📋 Interview Feedback")

    company_display = f" at {st.session_state['company']}" if st.session_state["company"] else ""
    st.markdown(
        f'<div class="info-box">'
        f'Performance review for <strong>{st.session_state["name"]}</strong> — '
        f'<strong>{st.session_state["level"]} {st.session_state["position"]}</strong>{company_display}'
        f'</div>',
        unsafe_allow_html=True
    )

    conversation_history = "\n".join([
        f"{msg['role'].upper()}: {msg['content']}"
        for msg in st.session_state.messages
        if msg["role"] != "system"
    ])

    feedback_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    with st.spinner("Generating your personalized feedback..."):
        feedback_completion = feedback_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are a senior talent evaluator providing honest, constructive feedback "
                        f"on a {st.session_state['interview_style']} interview for the role of "
                        f"{st.session_state['level']} {st.session_state['position']}.\n\n"
                        "Evaluate the candidate and respond ONLY with the following structured format:\n\n"
                        "Overall Score: [X/10]\n\n"
                        "## Strengths\n"
                        "- [Bullet point strengths from the interview]\n\n"
                        "## Areas for Improvement\n"
                        "- [Specific, actionable improvement areas]\n\n"
                        "## Recommendation\n"
                        "[Hire / Strong Hire / No Hire / Needs More Interview] with a 2-3 sentence justification.\n\n"
                        "## Top Tip\n"
                        "[One single most impactful thing they should work on before their next interview]\n\n"
                        "Do not add any preamble, sign-offs, or additional commentary outside this format."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Here is the full interview transcript to evaluate:\n\n{conversation_history}"
                    )
                }
            ]
        )

    feedback_text = feedback_completion.choices[0].message.content

    st.markdown(
        f'<div class="score-card">{feedback_text}</div>',
        unsafe_allow_html=True
    )

    st.divider()
    col_r, col_s = st.columns([1, 1])
    with col_r:
        if st.button("🔄 Start New Interview", type="primary", on_click=restart):
            pass
    with col_s:
        st.download_button(
            label="⬇️ Download Feedback",
            data=f"Interview Feedback — {st.session_state['name']}\n"
                 f"Role: {st.session_state['level']} {st.session_state['position']}\n"
                 f"Company: {st.session_state.get('company', 'N/A')}\n"
                 f"Industry: {st.session_state.get('industry', 'N/A')}\n"
                 f"Interview Style: {st.session_state['interview_style']}\n\n"
                 f"{'='*50}\n\n{feedback_text}",
            file_name=f"interview_feedback_{st.session_state['name'].replace(' ', '_').lower()}.txt",
            mime="text/plain"
        )