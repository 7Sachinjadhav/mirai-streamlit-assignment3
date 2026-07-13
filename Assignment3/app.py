import os
import time
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

st.set_page_config(
    page_title="The Multiverse of Chatbots",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# PERSONAS
# ----------------------------------------------------------------------------
PERSONAS = {
    "An Angry Ravi Shastri": {
        "emoji": "🏏",
        "tagline": "Ex-coach, full volume, zero filter.",
        "system_prompt": (
            "You are an extremely animated and slightly angry version of former Indian "
            "cricket coach Ravi Shastri commentating on everything with maximum drama. "
            "Use his catchphrases like 'tracer bullet', 'BOOM', and speak loudly in "
            "ALL-CAPS bursts occasionally. Be passionate, a bit grumpy, and very opinionated "
            "about cricket, but keep it fun and never genuinely offensive."
        ),
    },
    "An Expert Hacker": {
        "emoji": "💻",
        "tagline": "Terminal green text energy, speaks in tech jargon.",
        "system_prompt": (
            "You are a stereotypical elite hacker from a movie. You speak confidently in "
            "technical jargon, occasionally reference 'the mainframe', 'firewalls', and "
            "'zero-days', and treat every question like a system to be cracked. Be clever, "
            "a little mysterious, and helpful underneath the bravado. Never provide real "
            "malicious hacking instructions - keep it fictional and fun."
        ),
    },
    "A Crazy Ronaldo Fan": {
        "emoji": "⚽",
        "tagline": "SIUUUU energy in every reply.",
        "system_prompt": (
            "You are an obsessive, hyper-enthusiastic Cristiano Ronaldo superfan. You bring "
            "up Ronaldo's stats, GOAT debates, and his 'SIUUU' celebration in almost every "
            "answer, no matter the topic. Be funny, over-the-top, and endlessly loyal to "
            "Ronaldo, but still genuinely try to answer the user's question."
        ),
    },
    "A Wise Old Yoda": {
        "emoji": "🟢",
        "tagline": "Speaks in riddles, wisdom he has.",
        "system_prompt": (
            "You are Yoda, the wise Jedi Master. Speak in his distinctive inverted sentence "
            "structure, give short profound wisdom, and occasionally reference the Force. "
            "Be gentle, patient, and genuinely insightful."
        ),
    },
    "A Sarcastic Teenager": {
        "emoji": "🙄",
        "tagline": "Ugh, fine, I'll answer.",
        "system_prompt": (
            "You are a sarcastic, eye-rolling teenager who acts mildly annoyed at having to "
            "answer questions but is secretly quite smart. Use casual slang, dry humor, and "
            "playful sarcasm, while still giving a genuinely correct and useful answer."
        ),
    },
    "A Gordon Ramsay Chef": {
        "emoji": "🔥",
        "tagline": "It's RAW! Now let's cook.",
        "system_prompt": (
            "You are an intense, passionate chef in the style of Gordon Ramsay. You are "
            "blunt, dramatic, occasionally exasperated, and obsessed with quality and "
            "excellence in everything - not just food. Sprinkle in classic Ramsay-style "
            "exclamations. Keep insults playful and never genuinely cruel."
        ),
    },
    "A Shakespearean Poet": {
        "emoji": "🎭",
        "tagline": "Speaketh in verse and old English.",
        "system_prompt": (
            "You are a dramatic Shakespearean-era poet. Respond in flowery, old English "
            "style with 'thee', 'thou', 'doth', and occasional iambic rhythm, while still "
            "clearly answering the question asked."
        ),
    },
    "A Motivational Coach": {
        "emoji": "🔥",
        "tagline": "LET'S GOOO! You've got this!",
        "system_prompt": (
            "You are an extremely high-energy motivational coach. Every response is packed "
            "with encouragement, hype, and empowering language, pushing the user to feel "
            "unstoppable, while still giving a genuinely useful and correct answer."
        ),
    },
    "A Pirate Captain": {
        "emoji": "🏴‍☠️",
        "tagline": "Arrr, speak yer question, matey.",
        "system_prompt": (
            "You are a swashbuckling pirate captain. Speak with pirate slang like 'arrr', "
            "'matey', and 'ye', reference the high seas and treasure often, but still give "
            "a clear and useful answer to the question."
        ),
    },
}

# ----------------------------------------------------------------------------
# STYLES
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Space Grotesk', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 20% 20%, #1a1440 0%, #0b0b1a 45%, #050509 100%);
        color: #f0f0f0;
    }

    #MainMenu, footer, header {visibility: hidden;}

    .hero-title {
        font-size: 2.6rem;
        font-weight: 700;
        background: linear-gradient(90deg, #8b5cf6, #ec4899, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
        letter-spacing: -1px;
    }

    .hero-sub {
        color: #e0e0e0;
        font-size: 0.95rem;
        margin-top: 4px;
        margin-bottom: 1.6rem;
    }

    .persona-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(139, 92, 246, 0.12);
        border: 1px solid rgba(139, 92, 246, 0.35);
        padding: 8px 16px;
        border-radius: 999px;
        font-size: 0.85rem;
        color: #e8e8f8;
        margin-bottom: 1.2rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #100c26 0%, #0b0b1a 100%);
        border-right: 1px solid rgba(139, 92, 246, 0.15);
    }

    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #e8e8f8;
    }

    section[data-testid="stSidebar"] {
        color: #e0e0e0;
    }

    div[data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 4px 6px;
        color: #e0e0e0;
    }

    div[data-testid="stChatMessage"] p {
        color: #e0e0e0;
    }

    div[data-testid="stChatMessage"] code {
        background: rgba(255,255,255,0.08);
        color: #a8f5d8;
        padding: 2px 6px;
        border-radius: 4px;
    }

    .stChatInputContainer, div[data-testid="stChatInput"] {
        border-radius: 14px !important;
    }

    /* Make chat input text HIGHLY visible */
    .stChatInputContainer {
        background-color: rgba(50, 40, 80, 0.8) !important;
        padding: 10px !important;
        border-radius: 14px !important;
    }

    .stChatInputContainer input {
        color: #ffffff !important;
        background-color: rgba(20, 15, 40, 0.9) !important;
        font-size: 16px !important;
        padding: 12px !important;
    }

    .stChatInputContainer input::placeholder {
        color: #808080 !important;
    }

    input[type="text"] {
        color: #ffffff !important;
        background-color: rgba(20, 15, 40, 0.9) !important;
    }

    input[type="text"]::placeholder {
        color: #808080 !important;
    }

    textarea {
        color: #ffffff !important;
        background-color: rgba(20, 15, 40, 0.9) !important;
    }

    textarea::placeholder {
        color: #808080 !important;
    }

    .stButton>button {
        background: linear-gradient(90deg, #8b5cf6, #6366f1);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: transform 0.15s ease;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(139, 92, 246, 0.35);
    }

    div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.04);
        border-radius: 10px;
        border: 1px solid rgba(139, 92, 246, 0.25);
    }

    .status-pill {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .status-ok { background: rgba(34,197,94,0.15); color: #5edd95; border: 1px solid rgba(34,197,94,0.35); }
    .status-bad { background: rgba(239,68,68,0.15); color: #ff9898; border: 1px solid rgba(239,68,68,0.35); }

    /* Improve text visibility for all markdown content */
    [data-testid="stMarkdownContainer"] {
        color: #e0e0e0;
    }

    [data-testid="stMarkdownContainer"] p {
        color: #e0e0e0;
    }

    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4 {
        color: #f0f0f0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🌌 Multiverse")
    st.caption("Pick a personality, then chat.")

    persona_name = st.selectbox(
        "Who do you want to talk to?",
        list(PERSONAS.keys()),
        format_func=lambda p: f"{PERSONAS[p]['emoji']}  {p}",
    )
    st.markdown(
        f"<div class='persona-badge'>{PERSONAS[persona_name]['emoji']} "
        f"{PERSONAS[persona_name]['tagline']}</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    if API_KEY:
        st.markdown("**Gemini API:** <span class='status-pill status-ok'>Connected</span>", unsafe_allow_html=True)
    else:
        st.markdown("**Gemini API:** <span class='status-pill status-bad'>Missing key</span>", unsafe_allow_html=True)
        st.caption("Add `GEMINI_API_KEY=your_key` to the `.env` file, then restart the app.")

    st.caption(f"Model: `{MODEL_NAME}`")

    st.markdown("---")
    if st.button("🗑️ Clear this conversation", use_container_width=True):
        st.session_state.pop(f"history_{persona_name}", None)
        st.rerun()

    st.markdown("---")
    st.caption("Built with Streamlit + Gemini API")

# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.markdown("<div class='hero-title'>The Multiverse of Chatbots</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='hero-sub'>One app, endless personalities. Switch characters anytime — each keeps its own memory.</div>",
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# SESSION STATE (per-persona history)
# ----------------------------------------------------------------------------
history_key = f"history_{persona_name}"
if history_key not in st.session_state:
    st.session_state[history_key] = []

history = st.session_state[history_key]

# ----------------------------------------------------------------------------
# RENDER PAST MESSAGES
# ----------------------------------------------------------------------------
user_avatar = "🧑"
bot_avatar = PERSONAS[persona_name]["emoji"]

for msg in history:
    avatar = user_avatar if msg["role"] == "user" else bot_avatar
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ----------------------------------------------------------------------------
# GEMINI CALL
# ----------------------------------------------------------------------------
def get_model():
    return genai.Client(api_key=API_KEY)


# ----------------------------------------------------------------------------
# CHAT INPUT
# ----------------------------------------------------------------------------
placeholder_text = f"Say something to {persona_name}..."
user_input = st.chat_input(placeholder_text)

if user_input:
    if not API_KEY:
        st.error("No Gemini API key found. Add `GEMINI_API_KEY=your_key` to the `.env` file and restart the app.")
    else:
        # Show user message immediately
        with st.chat_message("user", avatar=user_avatar):
            st.markdown(user_input)
        history.append({"role": "user", "content": user_input})

        # Build Gemini-format contents (include the current user message)
        gemini_contents = []
        for m in history:
            role = "user" if m["role"] == "user" else "model"
            gemini_contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=m["content"])]
                )
            )

        try:
            client = get_model()

            with st.chat_message("assistant", avatar=bot_avatar):
                with st.spinner("Thinking..."):
                    # Get response stream from Gemini
                    response_stream = client.models.generate_content_stream(
                        model=MODEL_NAME,
                        contents=gemini_contents,
                        config=types.GenerateContentConfig(
                            system_instruction=PERSONAS[persona_name]["system_prompt"]
                        )
                    )
                    # Peek the first chunk to hide spinner when generation starts
                    try:
                        first_chunk = next(response_stream)
                    except StopIteration:
                        first_chunk = None

                # Stream the reply live to the chat
                def response_generator():
                    if first_chunk and first_chunk.text:
                        yield first_chunk.text
                    for chunk in response_stream:
                        if chunk.text:
                            yield chunk.text

                full_text = st.write_stream(response_generator())

            history.append(
                {
                    "role": "assistant",
                    "content": full_text,
                }
            )

        except Exception as e:
            import traceback

            traceback.print_exc()

            st.exception(e)

if not history:
    st.info(f"👋 Say hi to **{persona_name}** below to get started!")
