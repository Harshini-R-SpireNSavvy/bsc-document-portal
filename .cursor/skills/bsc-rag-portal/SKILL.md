---
name: bsc-rag-portal
description: >-
  Work on the BSC Document Portal Streamlit RAG app (login, document upload,
  ChromaDB indexing, Groq chat). Use when editing app.py, login_page.py, rag.py,
  auth.py, Streamlit UI/CSS, deployment, or document Q&A features.
---

# BSC Document Portal

## Architecture

| File | Role |
|------|------|
| `app.py` | Main Streamlit app: themes, header, sidebar, insights + chat UI |
| `login_page.py` | Login/signup/forgot UI and styles (no auth logic) |
| `auth.py` | Password hashing, `authenticate()`, `register_user()`, `users.json` |
| `rag.py` | Load/index PDF/DOCX/TXT/XLSX, ChromaDB, Groq RAG + chat |
| `documents/` | Uploaded files folder (indexed on load) |
| `.streamlit/config.toml` | Light base theme |
| `.streamlit/secrets.toml.example` | Template for cloud secrets |

## Environment / secrets

```toml
GROQ_API_KEY = "..."
APP_USERNAME = "admin"
APP_PASSWORD = "..."
APP_USERS = "user1:pass1,user2:pass2"  # optional
```

Local: `.env` (gitignored). Cloud: Streamlit **Secrets**.

## Conventions

- **Auth**: Do not weaken login checks. UI-only changes go in `login_page.py`.
- **Windows**: No emoji in `print()` in `rag.py` (use `[OK]`, `[ERROR]`, etc.).
- **Streamlit CSS**: Use `st.container(key="...")` + `.st-key-*` selectors; avoid broken HTML wrappers around widgets.
- **Theme**: `st.session_state.theme` is `"Light"` or `"Dark"`; `inject_styles()` in `app.py` must style sidebar, chat input, selects, and alerts for both.
- **Settings panel**: Top-right `st.popover("Settings")` in `render_top_bar()` — appearance + signed-in user.
- **Chat input**: Keep `st.chat_input` outside bordered containers so theming works.
- **Scope**: Minimal diffs; match existing Inter font and blue accent (`#2563eb`).

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Default login: `admin` / `admin123` (override via env).

## Deploy

- Repo: push to GitHub; main file `app.py`.
- **Streamlit Community Cloud**: [share.streamlit.io](https://share.streamlit.io) + secrets from example file.
- `deploy.ps1`: creates `bsc-document-portal` repo and pushes (requires `gh auth login`).

## RAG pipeline (`rag.py`)

1. `load_documents()` → chunk (300 words, 50 overlap) → `SentenceTransformer("all-MiniLM-L6-v2")`
2. ChromaDB in-memory collection `documents` (rebuilt on re-index)
3. `chat()` retrieves top 6 chunks, sends to Groq `llama-3.1-8b-instant`

If `GROQ_API_KEY` is missing, `chat()` returns a clear error string (no crash at import).

## Common tasks

| Task | Where to edit |
|------|----------------|
| Login look & feel | `login_page.py` only |
| Portal layout / dark mode | `app.py` `inject_styles`, `render_*` |
| New file type | `rag.py` `load_documents()` |
| New users | Sign up UI or `APP_USERS` / `users.json` |
| Cloud secrets | Streamlit dashboard, not committed files |
