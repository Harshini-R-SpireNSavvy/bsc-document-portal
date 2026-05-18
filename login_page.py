import streamlit as st

from auth import authenticate, register_user


def inject_login_styles():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

            [data-testid="stSidebar"],
            [data-testid="stHeader"],
            footer,
            #MainMenu {
                visibility: hidden;
                display: none;
            }

            .stApp {
                background: linear-gradient(180deg, #f8fafc 0%, #eef2f7 50%, #e2e8f0 100%);
                font-family: 'Inter', sans-serif;
            }

            .main .block-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: calc(100vh - 4rem);
                padding: 2rem 1rem 3rem;
                max-width: 100% !important;
            }

            .login-shell {
                width: 100%;
                min-width: 320px;
                max-width: 400px;
                margin: 0 auto;
                box-sizing: border-box;
            }

            .brand-wrap {
                text-align: center;
                margin: 0 0 2.25rem 0;
            }

            .brand-line1 {
                font-size: 3.5rem !important;
                font-weight: 700;
                color: #0f172a;
                letter-spacing: 0.08em;
                line-height: 1.1;
                margin: 0;
                white-space: nowrap;
            }

            .brand-line2 {
                font-size: 3.5rem !important;
                font-weight: 700;
                color: #2563eb;
                letter-spacing: 0.08em;
                line-height: 1.1;
                margin: 0.15rem 0 0 0;
                white-space: nowrap;
            }

            .login-shell [data-testid="stVerticalBlockBorderWrapper"] {
                background: #ffffff;
                border: 1px solid #e2e8f0 !important;
                border-radius: 16px !important;
                padding: 1.5rem 1.25rem 1.35rem !important;
                box-shadow: 0 8px 30px rgba(15, 23, 42, 0.08);
                width: 100%;
                box-sizing: border-box;
            }

            .login-shell div[data-testid="stTextInput"] {
                margin-bottom: 1rem !important;
                width: 100% !important;
            }

            .login-shell div[data-testid="stTextInput"] label,
            .login-shell div[data-testid="stTextInput"] > label {
                display: none !important;
            }

            .login-shell div[data-testid="stTextInput"] > div {
                width: 100% !important;
            }

            .login-shell div[data-testid="stTextInput"] input {
                width: 100% !important;
                box-sizing: border-box !important;
                background: #f8fafc !important;
                border: 1px solid #cbd5e1 !important;
                border-radius: 12px !important;
                color: #0f172a !important;
                padding: 12px 16px !important;
                font-size: 15px !important;
                min-height: 48px !important;
                line-height: 1.4 !important;
            }

            .login-shell div[data-testid="stTextInput"] input::placeholder {
                color: #94a3b8 !important;
            }

            .login-shell div[data-testid="stTextInput"] input:focus {
                border-color: #3b82f6 !important;
                box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
                background: #ffffff !important;
            }

            .login-shell .st-key-login_pass {
                margin-bottom: 0 !important;
            }

            .login-shell div[data-testid="stHorizontalBlock"]:has(.st-key-login_btn) {
                display: flex !important;
                flex-wrap: nowrap !important;
                gap: 12px !important;
                margin-top: 1.25rem !important;
                width: 100% !important;
            }

            .login-shell div[data-testid="stHorizontalBlock"]:has(.st-key-login_btn) > div {
                flex: 1 1 0 !important;
                min-width: 140px !important;
                width: auto !important;
            }

            .login-shell .st-key-login_btn,
            .login-shell .st-key-signup_btn,
            .login-shell .st-key-create_account,
            .login-shell .st-key-request_reset {
                flex: 1 1 0 !important;
                min-width: 140px !important;
            }

            .login-shell .st-key-login_btn .stButton,
            .login-shell .st-key-signup_btn .stButton,
            .login-shell .st-key-create_account .stButton,
            .login-shell .st-key-request_reset .stButton {
                width: 100% !important;
            }

            .login-shell .st-key-login_btn .stButton > button,
            .login-shell .st-key-signup_btn .stButton > button,
            .login-shell .st-key-create_account .stButton > button,
            .login-shell .st-key-request_reset .stButton > button {
                background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%) !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 12px !important;
                padding: 0 20px !important;
                font-weight: 600 !important;
                font-size: 16px !important;
                width: 100% !important;
                min-width: 140px !important;
                min-height: 48px !important;
                height: 48px !important;
                white-space: nowrap !important;
                overflow: hidden !important;
                text-overflow: ellipsis !important;
            }

            .login-shell .st-key-login_btn .stButton > button:hover,
            .login-shell .st-key-signup_btn .stButton > button:hover,
            .login-shell .st-key-create_account .stButton > button:hover,
            .login-shell .st-key-request_reset .stButton > button:hover {
                background: linear-gradient(180deg, #4f8ff7 0%, #3b82f6 100%) !important;
            }

            .login-shell .st-key-forgot_btn {
                display: flex !important;
                justify-content: center !important;
                width: 100% !important;
                margin-top: 1rem !important;
            }

            .login-shell .st-key-forgot_btn .stButton {
                width: auto !important;
            }

            .login-shell .st-key-forgot_btn .stButton > button {
                background: transparent !important;
                border: none !important;
                color: #64748b !important;
                font-size: 13px !important;
                font-weight: 400 !important;
                box-shadow: none !important;
                width: auto !important;
                min-width: unset !important;
                min-height: unset !important;
                height: auto !important;
                padding: 0.25rem 0.5rem !important;
                white-space: nowrap !important;
            }

            .login-shell .st-key-forgot_btn .stButton > button:hover {
                color: #2563eb !important;
                background: transparent !important;
                text-decoration: underline !important;
            }

            .login-shell .st-key-back_btn .stButton > button,
            .login-shell .st-key-signup_back .stButton > button {
                background: transparent !important;
                border: none !important;
                color: #64748b !important;
                font-size: 13px !important;
                white-space: nowrap !important;
            }

            .auth-msg {
                border-radius: 10px;
                padding: 0.75rem 1rem;
                margin-bottom: 1rem;
                font-size: 0.88rem;
            }

            .auth-msg.error {
                background: #fef2f2;
                border: 1px solid #fecaca;
                color: #b91c1c;
            }

            .auth-msg.success {
                background: #f0fdf4;
                border: 1px solid #bbf7d0;
                color: #15803d;
            }

            .auth-msg.info {
                background: #eff6ff;
                border: 1px solid #bfdbfe;
                color: #1d4ed8;
            }

            @media (max-width: 360px) {
                .brand-line1 { font-size: 2.75rem !important; }
                .brand-line2 { font-size: 2.75rem !important; }

                .login-shell div[data-testid="stHorizontalBlock"]:has(.st-key-login_btn) {
                    flex-direction: column !important;
                }

                .login-shell div[data-testid="stHorizontalBlock"]:has(.st-key-login_btn) > div {
                    min-width: 100% !important;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _auth_message(text: str, level: str = "error"):
    st.markdown(f'<div class="auth-msg {level}">{text}</div>', unsafe_allow_html=True)


def _login_shell(content_fn):
    inject_login_styles()
    _, panel, _ = st.columns([1, 1, 1])
    with panel:
        st.markdown('<div class="login-shell">', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="brand-wrap">
                <p class="brand-line1">BSC</p>
                <p class="brand-line2">AI</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.container(border=True):
            content_fn()
        st.markdown("</div>", unsafe_allow_html=True)


def render_login_page():
    mode = st.session_state.auth_mode

    if mode == "forgot":

        def forgot_content():
            st.markdown(
                '<p class="auth-msg info">Enter your username below. '
                "Password reset is managed by your administrator.</p>",
                unsafe_allow_html=True,
            )
            forgot_user = st.text_input(
                "forgot_user",
                placeholder="Email or Username",
                label_visibility="collapsed",
            )
            if st.button("Request reset", use_container_width=True, key="request_reset"):
                if forgot_user.strip():
                    _auth_message(
                        f"If an account exists for '{forgot_user.strip()}', "
                        "your administrator will be notified.",
                        "success",
                    )
                else:
                    _auth_message("Please enter your username.", "error")

            if st.button("Back to Login", key="back_btn"):
                st.session_state.auth_mode = "login"
                st.rerun()

        _login_shell(forgot_content)
        return

    if mode == "signup":

        def signup_content():
            signup_user = st.text_input(
                "signup_user",
                placeholder="Email or Username",
                label_visibility="collapsed",
            )
            signup_pass = st.text_input(
                "signup_pass",
                placeholder="Password",
                type="password",
                label_visibility="collapsed",
            )
            signup_confirm = st.text_input(
                "signup_confirm",
                placeholder="Confirm Password",
                type="password",
                label_visibility="collapsed",
            )

            if st.button("Create Account", use_container_width=True, key="create_account"):
                if not signup_user or not signup_pass:
                    _auth_message("Please fill in all fields.", "error")
                elif signup_pass != signup_confirm:
                    _auth_message("Passwords do not match.", "error")
                else:
                    ok, msg = register_user(signup_user, signup_pass)
                    if ok:
                        _auth_message(msg, "success")
                        st.session_state.auth_mode = "login"
                    else:
                        _auth_message(msg, "error")

            if st.button("Back to Login", key="signup_back"):
                st.session_state.auth_mode = "login"
                st.rerun()

        _login_shell(signup_content)
        return

    def login_content():
        username = st.text_input(
            "login_user",
            placeholder="Email or Username",
            label_visibility="collapsed",
        )
        password = st.text_input(
            "login_pass",
            placeholder="Password",
            type="password",
            label_visibility="collapsed",
        )

        btn_login, btn_signup = st.columns(2, gap="small")
        with btn_login:
            login_clicked = st.button("Login", use_container_width=True, type="primary", key="login_btn")
        with btn_signup:
            signup_clicked = st.button("Sign Up", use_container_width=True, key="signup_btn")

        if login_clicked:
            if not username or not password:
                _auth_message("Please enter both username and password.", "error")
            elif authenticate(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username.strip()
                st.session_state.auth_mode = "login"
                st.rerun()
            else:
                _auth_message("Invalid username or password.", "error")

        if signup_clicked:
            st.session_state.auth_mode = "signup"
            st.rerun()

        if st.button("Forgot password?", key="forgot_btn"):
            st.session_state.auth_mode = "forgot"
            st.rerun()

    _login_shell(login_content)
