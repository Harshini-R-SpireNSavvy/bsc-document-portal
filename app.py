import os

import streamlit as st

from login_page import render_login_page
from rag import chat, index_documents

st.set_page_config(
    page_title="BSC Document Portal",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "theme" not in st.session_state:
    st.session_state.theme = "Light"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"


def apply_theme():
    if st.session_state.theme == "Dark":
        return {
            "bg": "#0f172a",
            "surface": "#1e293b",
            "surface_alt": "#334155",
            "text": "#f1f5f9",
            "muted": "#94a3b8",
            "border": "#475569",
            "accent": "#3b82f6",
            "accent_hover": "#2563eb",
        }
    return {
        "bg": "#f8fafc",
        "surface": "#ffffff",
        "surface_alt": "#f1f5f9",
        "text": "#0f172a",
        "muted": "#64748b",
        "border": "#e2e8f0",
        "accent": "#1e40af",
        "accent_hover": "#1e3a8a",
    }


def inject_styles(theme: dict):
    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

            .stApp {{
                background-color: {theme["bg"]};
                font-family: 'Inter', sans-serif;
                color: {theme["text"]};
            }}

            .main .block-container {{
                padding-top: 1.75rem;
                padding-bottom: 5rem;
                max-width: 1080px;
            }}

            .main h1, .main h2, .main h3, .main h4,
            .main p, .main label, .main span,
            .main .stMarkdown {{
                color: {theme["text"]};
            }}

            .portal-header {{
                background: linear-gradient(135deg, {theme["accent"]} 0%, {theme["accent_hover"]} 100%);
                border-radius: 16px;
                padding: 2rem 2.25rem;
                margin-bottom: 2rem;
                margin-top: 0.25rem;
            }}

            .portal-brand {{
                display: flex;
                align-items: baseline;
                gap: 0.35rem;
                margin-bottom: 0.35rem;
            }}

            .portal-brand-bsc {{
                font-size: 2.25rem;
                font-weight: 800;
                color: #ffffff !important;
                letter-spacing: 0.06em;
                line-height: 1;
            }}

            .portal-brand-ai {{
                font-size: 2.25rem;
                font-weight: 800;
                color: #93c5fd !important;
                letter-spacing: 0.06em;
                line-height: 1;
            }}

            .portal-tagline {{
                color: rgba(255, 255, 255, 0.92) !important;
                font-size: 1rem;
                font-weight: 500;
                margin: 0 0 0.25rem 0;
            }}

            .portal-subtitle {{
                color: rgba(255, 255, 255, 0.78) !important;
                font-size: 0.92rem;
                margin: 0;
                line-height: 1.5;
            }}

            .st-key-top_settings_anchor {{
                position: fixed;
                top: 0.75rem;
                right: 1.25rem;
                z-index: 999;
                width: auto !important;
                height: 0;
                overflow: visible;
            }}

            .st-key-top_settings_anchor [data-testid="stPopover"] > button {{
                background: {theme["surface"]} !important;
                border: 1px solid {theme["border"]} !important;
                color: {theme["text"]} !important;
                border-radius: 10px !important;
                padding: 0.4rem 0.9rem !important;
                font-size: 0.85rem !important;
                font-weight: 500 !important;
                min-height: 36px !important;
                box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
            }}

            .st-key-top_settings_anchor label {{
                font-size: 0.78rem !important;
                color: {theme["muted"]} !important;
            }}

            .st-key-top_settings_anchor .meta-user-text {{
                font-size: 0.85rem;
                color: {theme["text"]};
                margin: 0.75rem 0 0 0;
                padding-top: 0.75rem;
                border-top: 1px solid {theme["border"]};
                line-height: 1.4;
            }}

            .st-key-top_settings_anchor .meta-user-text strong {{
                color: {theme["muted"]};
                font-weight: 500;
            }}

            section[data-testid="stSidebar"] > div {{
                background-color: {theme["surface"]} !important;
                border-right: 1px solid {theme["border"]};
            }}

            section[data-testid="stSidebar"] .stMarkdown,
            section[data-testid="stSidebar"] .stMarkdown p,
            section[data-testid="stSidebar"] label,
            section[data-testid="stSidebar"] h1,
            section[data-testid="stSidebar"] h2,
            section[data-testid="stSidebar"] h3,
            section[data-testid="stSidebar"] [data-testid="stText"],
            section[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
            section[data-testid="stSidebar"] .stCaption {{
                color: {theme["text"]} !important;
            }}

            section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{
                color: {theme["muted"]} !important;
            }}

            section[data-testid="stSidebar"] .stButton > button {{
                background-color: {theme["surface_alt"]} !important;
                color: {theme["text"]} !important;
                border: 1px solid {theme["border"]} !important;
            }}

            section[data-testid="stSidebar"] hr {{
                border-color: {theme["border"]} !important;
                margin: 1.25rem 0 !important;
            }}

            section[data-testid="stSidebar"] [data-testid="stAlert"] {{
                background-color: {theme["surface_alt"]} !important;
                color: {theme["text"]} !important;
                border: 1px solid {theme["border"]} !important;
            }}

            [data-testid="stVerticalBlockBorderWrapper"] {{
                background: {theme["surface"]} !important;
                border-color: {theme["border"]} !important;
                border-radius: 14px !important;
                padding: 0.35rem 0.15rem !important;
                margin-bottom: 1.75rem !important;
            }}

            .stButton > button {{
                border-radius: 10px;
                font-weight: 500;
                font-family: 'Inter', sans-serif;
            }}

            .stButton > button[kind="primary"] {{
                background-color: {theme["accent"]} !important;
                border-color: {theme["accent"]} !important;
                color: #ffffff !important;
            }}

            .stButton > button[kind="primary"]:hover {{
                background-color: {theme["accent_hover"]} !important;
                border-color: {theme["accent_hover"]} !important;
            }}

            .stButton > button[kind="secondary"] {{
                background-color: {theme["surface"]} !important;
                color: {theme["text"]} !important;
                border: 1px solid {theme["border"]} !important;
            }}

            div[data-baseweb="select"] > div {{
                background-color: {theme["surface"]} !important;
                color: {theme["text"]} !important;
                border-color: {theme["border"]} !important;
            }}

            div[data-testid="stTextInput"] input,
            div[data-testid="stTextArea"] textarea {{
                background-color: {theme["surface"]} !important;
                color: {theme["text"]} !important;
                border-color: {theme["border"]} !important;
            }}

            [data-testid="stFileUploader"] section {{
                background: {theme["surface_alt"]} !important;
                border: 1px dashed {theme["border"]} !important;
                border-radius: 12px !important;
            }}

            [data-testid="stFileUploader"] label,
            [data-testid="stFileUploader"] span,
            [data-testid="stFileUploader"] small {{
                color: {theme["text"]} !important;
            }}

            div[data-testid="stChatMessage"] {{
                background-color: {theme["surface"]} !important;
                border: 1px solid {theme["border"]} !important;
                border-radius: 12px !important;
                padding: 0.25rem 0.5rem !important;
                margin-bottom: 0.75rem !important;
            }}

            [data-testid="stBottomBlock"],
            [data-testid="stBottom"],
            [data-testid="stChatInput"],
            [data-testid="stChatInput"] > div,
            [data-testid="stChatInput"] section {{
                background-color: {theme["bg"]} !important;
            }}

            [data-testid="stChatInput"] {{
                border-top: 1px solid {theme["border"]} !important;
            }}

            [data-testid="stChatInput"] textarea {{
                background-color: {theme["surface"]} !important;
                color: {theme["text"]} !important;
                border: 1px solid {theme["border"]} !important;
                border-radius: 12px !important;
            }}

            [data-testid="stChatInput"] button {{
                background-color: {theme["accent"]} !important;
                color: #ffffff !important;
            }}

            .stAlert,
            [data-testid="stAlert"],
            [data-testid="stNotification"] {{
                background-color: {theme["surface_alt"]} !important;
                border: 1px solid {theme["border"]} !important;
                color: {theme["text"]} !important;
            }}

            [data-testid="stNotification"] p,
            [data-testid="stNotification"] span {{
                color: {theme["text"]} !important;
            }}

            div[data-baseweb="popover"] {{
                background-color: {theme["surface"]} !important;
                border: 1px solid {theme["border"]} !important;
                border-radius: 12px !important;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15) !important;
                min-width: 220px !important;
            }}

            div[data-baseweb="popover"] li,
            div[data-baseweb="popover"] span,
            div[data-baseweb="popover"] p {{
                color: {theme["text"]} !important;
            }}

            @media (max-width: 768px) {{
                .st-key-top_settings_anchor {{
                    position: fixed !important;
                    top: 0.5rem !important;
                    right: 0.75rem !important;
                }}
            }}

            hr {{
                border-color: {theme["border"]} !important;
                margin: 2rem 0 !important;
            }}

            .section-title {{
                margin-bottom: 0.35rem !important;
            }}

            .section-caption {{
                color: {theme["muted"]} !important;
                margin-bottom: 1.25rem !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )



def render_top_bar():
    with st.container(key="top_settings_anchor"):
        with st.popover("Settings"):
            theme_choice = st.selectbox(
                "Appearance",
                ["Light", "Dark"],
                index=0 if st.session_state.theme == "Light" else 1,
            )
            if theme_choice != st.session_state.theme:
                st.session_state.theme = theme_choice
                st.rerun()
            st.markdown(
                f'<p class="meta-user-text"><strong>Signed in as</strong><br>{st.session_state.username}</p>',
                unsafe_allow_html=True,
            )


def render_header():
    st.markdown(
        """
        <div class="portal-header">
            <div class="portal-brand">
                <span class="portal-brand-bsc">BSC</span>
                <span class="portal-brand-ai">AI</span>
            </div>
            <p class="portal-tagline">Document Intelligence Portal</p>
            <p class="portal-subtitle">Upload documents and query your knowledge base with AI-assisted analysis</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_sidebar():
    with st.sidebar:
        st.header("Document Management")
        st.caption("Supported formats: PDF, DOCX, TXT, XLSX")

        uploaded_files = st.file_uploader(
            "Upload files",
            type=["pdf", "docx", "txt", "xlsx", "xls"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

        if uploaded_files:
            os.makedirs("documents", exist_ok=True)
            for uploaded_file in uploaded_files:
                save_path = os.path.join("documents", uploaded_file.name)
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"Uploaded: {uploaded_file.name}")

            if st.button("Re-index documents", use_container_width=True):
                st.cache_resource.clear()
                st.rerun()

        st.divider()
        st.subheader("Indexed documents")

        docs_folder = "documents"
        if os.path.exists(docs_folder):
            files = [
                f
                for f in os.listdir(docs_folder)
                if f.endswith((".pdf", ".docx", ".txt", ".xlsx", ".xls"))
            ]
            if files:
                for name in sorted(files):
                    st.text(f"• {name}")
            else:
                st.caption("No documents uploaded yet.")
        else:
            st.caption("No documents uploaded yet.")

        st.divider()

        if st.button("Clear conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.divider()

        if st.button("Sign out", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.messages = []
            st.session_state.auth_mode = "login"
            st.rerun()


@st.cache_resource
def load_and_index():
    os.makedirs("documents", exist_ok=True)
    index_documents("documents")
    return True


def render_main_app(theme: dict):
    inject_styles(theme)
    render_top_bar()
    render_header()
    render_sidebar()

    load_and_index()

    with st.container(border=True):
        st.subheader("Document insights")
        st.caption("Generate a structured summary across all indexed documents.")

        if st.button("Generate insights report", type="primary", use_container_width=True):
            with st.spinner("Analyzing documents..."):
                insights = chat(
                    """Please analyse all the documents and provide:
                    1. A brief summary of each document
                    2. Key topics covered
                    3. Important dates, numbers or names mentioned
                    4. Any important clauses or action items
                    Keep it clear and structured."""
                )
            st.info(insights)

    st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.subheader("Document assistant")
        st.caption("Ask questions about your uploaded documents.")

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Type your question here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                response = chat(prompt)
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})


theme = apply_theme()

if not st.session_state.authenticated:
    render_login_page()
else:
    render_main_app(theme)
