📚 LibraryLLM – Your AI-Powered Book Assistant
LibraryLLM is a Streamlit-based app that lets users chat with a local language model (LLM) to get book summaries, author info, and personalized reading recommendations. It also offers daily quotes, book highlights, and a clean dark/light toggle.

LIVE DEMO - https://prabhasg-lib-llms.hf.space

## 🚀 Features

- 💬 **Chat Assistant** — Ask anything about books, authors, summaries.
- 📘 **Book Metadata** — Instantly get book details and links via OpenLibrary.
- 🧠 **LLM-Powered** — Uses Groq API with LLaMA models for smart responses.
- 📚 **Daily Book & Quote** — Motivational quotes and book picks updated daily.
- 🎯 **Reading Goals Tracker** — Set and track monthly reading goals.
- 🌙 **Dark Mode Toggle** — Dynamic theme with sidebar toggle.
- 📥 **Chat History & PDF Export** — Local session logs and downloadable responses.
- 🔧 **Prompt Presets** — Instant commands for summary, author info, etc.

---

## 🛠️ Tech Stack

| Component         | Tech                              |
|------------------|-----------------------------------|
| Frontend         | [Streamlit](https://streamlit.io) |
| LLM Backend      | [Groq API](https://groq.com/)     |
| Book Data Source | [OpenLibrary API](https://openlibrary.org/developers/api) |
| PDF Generation   | [FPDF](https://pyfpdf.github.io)  |

---

## 🧩 File Structure



📦 LibraryLLM
├── streamlit\_app.py      # Main app logic and UI
├── utils.py              # LLM logic, quotes, book generator
├── requirements.txt      # Python dependencies
├── Dockerfile            # Optional: for containerization
├── README.md             # Project documentation
└── .streamlit/
└── secrets.toml      # Groq API Key




## 🧪 Setup & Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/your-username/LibraryLLM.git
cd LibraryLLM
````

### 2. Create virtual environment (optional)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Groq API Key

Create a file: `.streamlit/secrets.toml`

```toml
GROQ_API_KEY = "your-groq-api-key"
```

### 5. Run the app

```bash
streamlit run streamlit_app.py
```

---

## 🌍 Deployment

Deploy on [Hugging Face Spaces](https://huggingface.co/spaces):

* Upload your project files.
* Set `streamlit_app.py` as your app entry point.
* Add your secrets in `hf_space.yml` or Secrets Manager.


## 📜 License

This project is licensed under the [MIT License](LICENSE).
