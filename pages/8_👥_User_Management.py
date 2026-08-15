import streamlit as st
import pandas as pd

from utils.auth import require_role
from utils.database import add_user, get_connection
from utils.ui import load_css


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="User Management | Agentic FacilityOps",
    page_icon="👥",
    layout="wide"
)

load_css()

require_role(["Employee"])


# ============================================================
# HEADER
# ============================================================

st.title("👥 User Management")

st.caption(
    "Create and manage Employee and Technician accounts."
)


# ============================================================
# ADD USER
# ============================================================

st.subheader("➕ Add New User")

with st.container(border=True):

    with st.form("add_user_form"):

        col1, col2 = st.columns(2)

        with col1:

            name = st.text_input(
                "Full Name",
                placeholder="Enter full name"
            )

            username = st.text_input(
                "Username",
                placeholder="Enter username"
            )

        with col2:

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password"
            )

            role = st.selectbox(
                "Role",
                [
                    "Employee",
                    "Technician"
                ]
            )

        submitted = st.form_submit_button(
            "➕ Add User",
            type="primary",
            use_container_width=True
        )


if submitted:

    if not name.strip():
        st.error("Please enter the user's name.")

    elif not username.strip():
        st.error("Please enter a username.")

    elif not password:
        st.error("Please enter a password.")

    else:

        success, message = add_user(
            username=username,
            password=password,
            name=name,
            role=role
        )

        if success:

            st.success(
                f"✅ {name} was added as {role}."
            )

            st.rerun()

        else:

            st.error(
                f"❌ {message}"
            )

with get_connection() as conn:

    users_df = pd.read_sql_query(
        """
        SELECT id, username, name, role
        FROM users
        ORDER BY id
        """,
        conn
    )


# ============================================================
# EXISTING USERS
# ============================================================

st.divider()

st.subheader("👥 Registered Users")

with get_connection() as conn:

    users_df = pd.read_sql_query(
        """
        SELECT
            id,
            name,
            username,
            role
        FROM users
        ORDER BY role, name
        """,
        conn
    )


if users_df.empty:

    st.info("No users found.")

else:

    st.dataframe(
        users_df,
        hide_index=True,
        use_container_width=True
    )