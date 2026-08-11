import streamlit as st
from utils.database import authenticate_user
from utils.ui import *
from utils.cards import *
from utils.charts import *
from utils.themes import *


load_css()
# --------------------------------------------------
# Session State
# --------------------------------------------------

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_role" not in st.session_state:
    st.session_state.user_role = None

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "username" not in st.session_state:
    st.session_state.username = None


# --------------------------------------------------
# Login Header
# --------------------------------------------------

st.markdown(
    """
    <div style="
        text-align: center;
        padding: 35px 0 10px 0;
    ">
        <h1 style="
            font-size: 42px;
            margin: 0;
            font-weight: 700;
        ">
            🏢 Agentic FacilityOps
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; font-size:18px; margin-top:5px;'>"
    "Facility Operations Management Platform"
    "</p>",
    unsafe_allow_html=True
)


# --------------------------------------------------
# Hide Sidebar
# --------------------------------------------------

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }

        [data-testid="collapsedControl"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Compact Login Card
# --------------------------------------------------

left, center, right = st.columns([1, 2, 1])

with center:

    with st.container(border=True):

        st.markdown(
            """
            <div style="text-align:center; margin-bottom:20px;">
                <h2 style="margin-bottom:5px;">🔐 Sign In</h2>
                <p style="margin:0; opacity:0.7;">
                    Access your FacilityOps account
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        role = st.radio(
            "Login as",
            ["Employee", "Technician"],
            horizontal=True
        )

        username = st.text_input(
            "Username",
            placeholder="Enter your username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        st.write("")

        if st.button(
            "Login",
            type="primary",
            use_container_width=True
        ):

            if not username.strip() or not password.strip():

                st.error(
                    "Please enter username and password."
                )

            else:

                demo_users = {
                    "john": {
                        "password": "tech123",
                        "name": "John Smith",
                        "role": "Technician"
                    },

                    "sarah": {
                        "password": "tech123",
                        "name": "Sarah Wilson",
                        "role": "Technician"
                    },

                    "david": {
                        "password": "tech123",
                        "name": "David Lee",
                        "role": "Technician"
                    },

                    "michael": {
                        "password": "tech123",
                        "name": "Michael Brown",
                        "role": "Technician"
                    },

                    "employee": {
                        "password": "employee123",
                        "name": "Facility Employee",
                        "role": "Employee"
                    }

                }

                user = demo_users.get(
                    username.lower()
                )

                if user and user["password"] == password:

                    if user["role"] != role:

                        st.error(
                            f"This account is registered as {user['role']}."
                        )

                    else:

                        st.session_state.authenticated = True
                        st.session_state.user_role = user["role"]
                        st.session_state.user_name = user["name"]
                        st.session_state.username = username

                        st.success("Login successful!")

                        st.rerun()

                else:

                    st.error(
                        "Invalid username or password."
                    )