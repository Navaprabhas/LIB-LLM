import os
import uuid
import json
import random
import requests
import streamlit as st
from datetime import datetime
from fpdf import FPDF
from utils import run_llm

# === CONFIG ===
MODEL_OPTIONS = ["llama3-8b-8192", "llama3-70b-8192"]
LANG_OPTIONS = ["English", "Spanish", "French", "German", "Hindi"]
PROMPT_PRESETS = {
    "Find author info": "Who wrote this book and when?",
    "Get summary": "Give me a short summary of this book.",
    "Suggest similar": "Suggest similar books based on this one."
}

# === DATA ===
QUOTES = [
    "A reader lives a thousand lives before he dies. – George R.R. Martin",
    "So many books, so little time. – Frank Zappa",
    "Reading is essential for those who seek to rise. – Frederick Douglass"
]
DAILY_BOOKS = ["The Hobbit", "1984", "To Kill a Mockingbird", "Sapiens", "The Alchemist"]

# === HELPERS ===
def extract_topic_from_prompt(prompt: str) -> str:
    stopwords = ["suggest", "recommend", "books", "for", "me", "on", "about", "give", "some", "good"]
    words = prompt.lower().split()
    keywords = [w for w in words if w not in stopwords]
    return " ".join(keywords) if keywords else prompt


def get_book_links(topic: str) -> list:
    try:
        res = requests.get("https://openlibrary.org/search.json", params={"q": topic}, timeout=10)
        docs = res.json().get("docs", [])[:5]
        return [{
            "title": b.get("title", "Unknown Title"),
            "author": ", ".join(b.get("author_name", ["Unknown"])),
            "link": f"https://openlibrary.org{b.get('key')}"
        } for b in docs]
    except:
        return []


def save_json(path: str, data):
    with open(path, "w") as f:
        json.dump(data, f)


def load_json(path: str, default):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default

# === SESSION ===
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

session_id = st.session_state.session_id
CHAT_HISTORY_PATH = f"/tmp/chat_history_{session_id}.json"
chat_history = load_json(CHAT_HISTORY_PATH, [])

# === UI Helpers ===
def theme_toggle():
    mode = st.sidebar.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    st.session_state.dark_mode = mode


def show_reading_goals():
    with st.sidebar.expander("🎯 My Reading Goals", expanded=True):
        total = st.slider("Books this month", 1, 30, 5)
        done = st.slider("Completed", 0, total, 1)
        col1, col2 = st.columns(2)
        col1.metric("Goal", f"{total}")
        col2.metric("Done", f"{done}")
        st.progress(done / total)


def show_daily_inspiration():
    with st.sidebar.container():
        today = datetime.now().day
        book = DAILY_BOOKS[today % len(DAILY_BOOKS)]
        quote = random.choice(QUOTES)
        st.markdown(f"**📘 {book}**")
        st.markdown(f"_{quote}_")

# === SIDEBAR ===
with st.sidebar:
    st.header("⚙️ Settings")
    theme_toggle()
    model = st.selectbox("Model", MODEL_OPTIONS)
    language = st.selectbox("Language", LANG_OPTIONS)
    with st.expander("🍀 Prompt Presets"):
        preset = st.selectbox("Preset", ["None"] + list(PROMPT_PRESETS.keys()))
        if st.button("🎲 Surprise Me"):
            st.session_state["user_prompt"] = random.choice(list(PROMPT_PRESETS.values()))

# === MAIN UI ===
st.title("📚 LibraryLLM")
st.caption("Your smart companion for discovering, learning, and chatting.")

tabs = st.tabs(["💬 Chat Assistant", "📘 Book Metadata"])

# --- Chat Assistant ---
with tabs[0]:
    for msg in chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    if prompt := st.chat_input("Ask about books, summaries, or authors..."):
        chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = run_llm(prompt, model)
                st.markdown(reply)
        chat_history.append({"role": "assistant", "content": reply})
        save_json(CHAT_HISTORY_PATH, chat_history)

# --- Book Metadata ---
with tabs[1]:
    title = st.text_input("Enter book title:")
    if title:
        with st.spinner():
            results = get_book_links(title)
        if results:
            for b in results:
                st.markdown(f"- **[{b['title']}]({b['link']})**  by {b['author']}")
        else:
            st.warning("No books found.")