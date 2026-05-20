---
title: BSC Document Portal
emoji: 📋
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: "1.28.0"
app_file: app.py
pinned: false
startup_duration_timeout: 45m
---

# BSC Document Portal

Streamlit RAG chatbot for uploading documents (PDF, DOCX, TXT, XLSX) and asking questions with AI-assisted answers powered by [Groq](https://groq.com) and local embeddings.

## Features

- Secure login with sign-up and password reset flow
- Document upload and automatic indexing
- Document insights report (summaries across all files)
- Conversational Q&A with source-aware RAG
- Light / dark theme (Settings popover, top right)

## Deploy on Hugging Face Spaces (free)

### Option A — Create Space from GitHub (recommended)

1. Open [huggingface.co/new-space](https://huggingface.co/new-space)
2. **Space name:** e.g. `bsc-document-portal`
3. **License:** your choice
4. **SDK:** Streamlit
5. Under **Create from**, choose **Link to existing repository** (or duplicate after push)
   - Repo: `Harshini-R-SpireNSavvy/bsc-document-portal`
6. Click **Create Space**

### Option B — Push this folder to a new HF Space

```bash
pip install huggingface_hub
huggingface-cli login
huggingface-cli repo create bsc-document-portal --type space --space_sdk streamlit
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/bsc-document-portal
git push hf main
```

### Add secrets (required)

In your Space → **Settings** → **Repository secrets**, add:

| Name | Value |
|------|--------|
| `GROQ_API_KEY` | Your key from [console.groq.com](https://console.groq.com) |
| `APP_USERNAME` | Login username (e.g. `admin`) |
| `APP_PASSWORD` | Strong password |

Optional: `APP_USERS` = `user1:pass1,user2:pass2`

Rebuild the Space after saving secrets.

### HF notes

- First build can take **10–20 minutes** (downloads embedding model).
- Free **CPU basic** may be tight on RAM; upgrade hardware in Space settings if the app crashes.
- Uploaded documents are **not persisted** across restarts on free Spaces.

---

## Quick start (local)

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
APP_USERNAME=admin
APP_PASSWORD=your_secure_password
```

### 3. Run the app

```bash
streamlit run app.py
```

Open `http://localhost:8501` and sign in.

## Project structure

```
app.py              # Main application
login_page.py       # Login / sign-up UI
auth.py             # Authentication helpers
rag.py              # Document loading, indexing, chat
documents/          # Uploaded files (created automatically)
.streamlit/         # Streamlit config
requirements.txt
```

## Deploy on Streamlit Cloud (alternative)

1. [share.streamlit.io](https://share.streamlit.io) → **Create app** → repo `bsc-document-portal` → `app.py`
2. Add secrets (same variable names as HF above).

## Configuration

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Required. Groq API key for LLM chat |
| `APP_USERNAME` | Default admin username (default: `admin`) |
| `APP_PASSWORD` | Default admin password (default: `admin123`) |
| `APP_USERS` | Optional extra users: `user1:pass1,user2:pass2` |

## Supported documents

- PDF (`.pdf`), Word (`.docx`), Text (`.txt`), Excel (`.xlsx`, `.xls`)

## Security

Never commit `.env` or API keys. Rotate keys if exposed.
