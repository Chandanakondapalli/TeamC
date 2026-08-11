import streamlit as st


def is_authenticated():
    return st.session_state.get("authenticated", False)


def require_login():

    if not is_authenticated():

        st.switch_page("pages/0_🔐_Login.py")


def logout():

    st.session_state.clear()

    st.switch_page("pages/0_🔐_Login.py")


def require_role(allowed_roles):
    require_login()

    role = st.session_state.get("user_role")

    if role not in allowed_roles:
        st.error("🚫 You do not have permission to access this page.")
        st.stop()


def get_role():
    return st.session_state.get("user_role")


def get_user_name():
    return st.session_state.get("user_name")

def hide_login_from_sidebar():
    """
    Hide the Login page from Streamlit's sidebar
    after the user has successfully logged in.
    """

    if is_authenticated():
        st.markdown(
            """
            <style>
            /* Hide Login page from sidebar after authentication */
            [data-testid="stSidebarNav"] a[href*="Login"] {
                display: none !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )