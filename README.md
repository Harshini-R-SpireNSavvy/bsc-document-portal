# BSC Document Portal

Streamlit RAG chatbot for uploading documents (PDF, DOCX, TXT, XLSX) and asking questions with AI-assisted answers powered by [Groq](https://groq.com) and local embeddings.

## Features

- Secure login with sign-up and password reset flow
- Document upload and automatic indexing
- Document insights report (summaries across all files)
- Conversational Q&A with source-aware RAG
- Light / dark theme (Settings popover, top right)

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

Get a free API key at [console.groq.com](https://console.groq.com).

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
.streamlit/         # Streamlit config and secrets example
requirements.txt
deploy.ps1          # Push to GitHub (optional)
```

## Deploy on Streamlit Cloud (free)

1. Fork or use this repo on GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. **Create app** → select this repo → **Main file:** `app.py` → **Branch:** `main`.
4. Add **Secrets** (Settings → Secrets):

```toml
GROQ_API_KEY = "your_groq_api_key"
APP_USERNAME = "admin"
APP_PASSWORD = "your_strong_password"
```

5. Deploy. First build may take 5–10 minutes (embedding model download).

### Push with script (Windows)

```powershell
gh auth login
.\deploy.ps1
```

## Configuration

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Required. Groq API key for LLM chat |
| `APP_USERNAME` | Default admin username (default: `admin`) |
| `APP_PASSWORD` | Default admin password (default: `admin123`) |
| `APP_USERS` | Optional extra users: `user1:pass1,user2:pass2` |

Sign-up stores additional users in `users.json` (local/ephemeral on free cloud hosts).

## Supported documents

- PDF (`.pdf`)
- Word (`.docx`)
- Text (`.txt`)
- Excel (`.xlsx`, `.xls`)

## Notes

- **Free tier**: Uploaded files may not persist after app restart on Streamlit Cloud.
- **Memory**: Embedding model loads at startup; allow time on first deploy.
- **Security**: Never commit `.env` or real API keys. Rotate keys if exposed.

## License

Private / internal use — adjust as needed for your organization.
