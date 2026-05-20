# Agent instructions

When working in this repository, read **`.cursor/skills/bsc-rag-portal/SKILL.md`** for architecture, env vars, UI conventions, and deployment notes.

## Priorities

1. Keep auth logic in `auth.py`; login styling in `login_page.py`.
2. Keep Streamlit light/dark themes consistent (sidebar, chat bar, inputs).
3. Avoid emoji in terminal `print` output (Windows encoding).
4. Do not commit `.env`, `users.json`, or secrets.

## Main entrypoint

```bash
streamlit run app.py
```
