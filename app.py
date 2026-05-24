import streamlit as st
from openai import OpenAI
import tempfile
import os

# ─────────────────────────────────────────────
# Page configuration
# ─────────────────────────────────────────────
st.set_page_config(page_title="AI Interview Tool", page_icon="🎙️")
st.title("🎙️ AI Interview Tool")

# ─────────────────────────────────────────────
# Session state initialization
# ─────────────────────────────────────────────
defaults = {
    "setup_complete": False,
    "user_message_count": 0,
    "feedback_shown": False,
    "chat_complete": False,
    "messages": [],
    "name": "",
    "experience": "",
    "skills": "",
    "level": "Junior",
    "position": "Data Scientist",
    "company": "Amazon",
    "input_mode": "Text",          # "Text" or "Voice"
    "voice_transcript": "",        # Holds the latest Whisper transcript
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ─────────────────────────────────────────────
# Helper callbacks
# ─────────────────────────────────────────────
def complete_setup():
    st.session_state.setup_complete = True

def show_feedback():
    st.session_state.feedback_shown = True

def transcribe_audio(audio_bytes: bytes) -> str:
    """Send audio bytes to OpenAI Whisper and return the transcript."""
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name
    try:
        with open(tmp_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text",
            )
        return transcript.strip()
    finally:
        os.unlink(tmp_path)

# ─────────────────────────────────────────────
# STAGE 1 — Setup
# ─────────────────────────────────────────────
if not st.session_state.setup_complete:

    st.subheader("👤 Personal Information")
    st.session_state["name"] = st.text_input(
        "Name", value=st.session_state["name"],
        placeholder="Enter your name", max_chars=40
    )
    st.session_state["experience"] = st.text_area(
        "Experience", value=st.session_state["experience"],
        placeholder="Describe your experience", max_chars=200
    )
    st.session_state["skills"] = st.text_area(
        "Skills", value=st.session_state["skills"],
        placeholder="List your skills", max_chars=200
    )

    st.subheader("🏢 Company and Position")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state["level"] = st.radio(
            "Choose level",
            options=["Junior", "Mid-level", "Senior"],
            index=["Junior", "Mid-level", "Senior"].index(st.session_state["level"])
        )
    with col2:
        positions = ("Data Scientist", "Data Engineer", "ML Engineer", "BI Analyst", "Financial Analyst")
        st.session_state["position"] = st.selectbox(
            "Choose a position", positions,
            index=positions.index(st.session_state["position"])
        )

    companies = ("Amazon", "Meta", "Udemy", "365 Company", "Nestle", "LinkedIn", "Spotify")
    st.session_state["company"] = st.selectbox(
        "Select a Company", companies,
        index=companies.index(st.session_state["company"])
    )

    st.subheader("🎙️ Response Mode")
    st.session_state["input_mode"] = st.radio(
        "How would you like to respond during the interview?",
        options=["Text", "Voice (Whisper)"],
        horizontal=True,
        help="Voice mode records your spoken answer and transcribes it automatically via OpenAI Whisper."
    )

    if st.button("Start Interview", on_click=complete_setup):
        st.write("Setup complete. Starting interview...")

# ─────────────────────────────────────────────
# STAGE 2 — Interview
# ─────────────────────────────────────────────
if st.session_state.setup_complete and not st.session_state.feedback_shown and not st.session_state.chat_complete:

    st.info("Start by introducing yourself", icon="👋")

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o"

    # Build system prompt on first load
    if not st.session_state.messages:
        st.session_state.messages = [{
            "role": "system",
            "content": (
                f"You are an HR executive that interviews an interviewee called {st.session_state['name']} "
                f"with experience {st.session_state['experience']} and skills {st.session_state['skills']}. "
                f"You should interview them for the position {st.session_state['level']} {st.session_state['position']} "
                f"at the company {st.session_state['company']}."
            )
        }]

    # Render chat history (skip system message)
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # ── Input area ─────────────────────────────
    prompt = None

    if st.session_state.user_message_count < 5:

        use_voice = st.session_state["input_mode"] == "Voice (Whisper)"

        if use_voice:
            # ── Voice mode ──
            st.markdown("**🎙️ Voice Mode** — Record your answer below:")
            audio_data = st.audio_input(
                label="Click to record your response",
                key=f"audio_input_{st.session_state.user_message_count}"
            )

            if audio_data is not None:
                with st.spinner("Transcribing with Whisper..."):
                    transcript = transcribe_audio(audio_data.getvalue())

                if transcript:
                    st.success(f"📝 **Transcript:** {transcript}")
                    # Use a button to confirm and submit the transcript
                    if st.button("✅ Submit this response", key=f"submit_{st.session_state.user_message_count}"):
                        prompt = transcript
                else:
                    st.warning("Whisper couldn't catch that — silence is golden but unhelpful here. Try again.")

        else:
            # ── Text mode ──
            if typed := st.chat_input("Your response", max_chars=1000):
                prompt = typed

    # ── Process submitted prompt ────────────────
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if st.session_state.user_message_count < 4:
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

        st.session_state.user_message_count += 1

        if st.session_state.user_message_count >= 5:
            st.session_state.chat_complete = True
            st.rerun()

# ─────────────────────────────────────────────
# STAGE 3 — Get Feedback button
# ─────────────────────────────────────────────
if st.session_state.chat_complete and not st.session_state.feedback_shown:
    st.info("Interview complete! Ready to see how you did?", icon="🏁")
    if st.button("Get Feedback", on_click=show_feedback):
        st.write("Fetching feedback...")

# ─────────────────────────────────────────────
# STAGE 4 — Feedback display
# ─────────────────────────────────────────────
if st.session_state.feedback_shown:

    st.subheader("📊 Interview Feedback")

    conversation_history = "\n".join([
        f"{msg['role']}: {msg['content']}"
        for msg in st.session_state.messages
    ])

    feedback_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    feedback_completion = feedback_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful tool that provides feedback on an interviewee's performance. "
                    "Before the feedback, give a score of 1 to 10. "
                    "Follow this format:\n\n"
                    "Overall Score: //Your score\n\n"
                    "Feedback: //Your detailed feedback\n\n"
                    "Give only the feedback — do not ask any additional questions."
                )
            },
            {
                "role": "user",
                "content": (
                    f"This is the interview you need to evaluate. "
                    f"Keep in mind that you are only a tool and should not engage in conversation: {conversation_history}"
                )
            }
        ]
    )

    st.write(feedback_completion.choices[0].message.content)

    st.divider()
    if st.button("🔄 Restart Interview", type="primary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()