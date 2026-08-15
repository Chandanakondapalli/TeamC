import streamlit as st

from login_database import authenticate


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Infosys Agentic FacilityOps AI Platform",
    page_icon="🏭",
    layout="centered"
)


# =====================================================
# SESSION STATE
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""


# =====================================================
# LOGIN PAGE
# =====================================================

if not st.session_state.logged_in:

    st.markdown(
        """
        <style>

        [data-testid="stSidebar"] {
            display: none;
        }

        .login-title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            margin-top: 60px;
        }

        .login-subtitle {
            text-align: center;
            color: #666;
            font-size: 18px;
            margin-bottom: 40px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="login-title">
            🏭 Infosys Agentic FacilityOps AI Platform
        </div>

        <div class="login-subtitle">
            AI-powered Predictive Maintenance Platform
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # =================================================
    # LOGIN
    # =================================================

    st.subheader("🔐 Login")

    username = st.text_input(
        "Username",
        placeholder="Enter username"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password"
    )

    if st.button(
        "🔑 Login",
        use_container_width=True,
        type="primary"
    ):

        user = authenticate(
            username.strip(),
            password
        )

        if user:

            st.session_state.logged_in = True

            st.session_state.username = user[0]

            st.session_state.role = user[1]

            st.success(
                f"Welcome {user[0]}!"
            )

            st.rerun()

        else:

            st.error(
                "❌ Invalid username or password."
            )


    # =================================================
    # DEMO ACCOUNTS
    # =================================================

    st.markdown("---")

   
# =====================================================
# AFTER LOGIN
# =====================================================

else:

    username = st.session_state.username

    role = st.session_state.role


    # =================================================
    # CREATE ROLE-BASED NAVIGATION
    # =================================================

    if role == "Admin":

        pages = {

            "Main": [
                st.Page(
                    "pages/Home.py",
                    title="Home",
                    icon="🏠"
                )
            ],

            "Analysis": [

                st.Page(
                    "pages/eda.py",
                    title="EDA",
                    icon="📊"
                ),

                st.Page(
                    "pages/dashboard.py",
                    title="Dashboard",
                    icon="📈"
                )

            ],

            "Machine": [

                st.Page(
                    "pages/3_Machine_Explorer.py",
                    title="Machine Explorer",
                    icon="🏭"
                )

            ],

            "AI": [

                st.Page(
                    "pages/4_AI_Assistant.py",
                    title="AI Assistant",
                    icon="🤖"
                )

            ],

            "Work Orders": [

                st.Page(
                    "pages/5_Work_Order_Creation.py",
                    title="Work Order Creation",
                    icon="📝"
                ),

                st.Page(
                    "pages/6_Work_Order_Management.py",
                    title="Work Order Management",
                    icon="📋"
                )

            ],

            "Maintenance": [

                st.Page(
                    "pages/7_Preventive_Maintenance.py",
                    title="Preventive Maintenance",
                    icon="🗓️"
                )

            ]

        }


    elif role == "Technician":

        pages = {

            "Main": [

                st.Page(
                    "pages/Home.py",
                    title="Home",
                    icon="🏠"
                )

            ],

            "Machine": [

                st.Page(
                    "pages/3_Machine_Explorer.py",
                    title="Machine Explorer",
                    icon="🏭"
                )

            ],

            "AI": [

                st.Page(
                    "pages/4_AI_Assistant.py",
                    title="AI Assistant",
                    icon="🤖"
                )

            ],

            "Work": [

                st.Page(
                    "pages/6_Work_Order_Management.py",
                    title="My Work Orders",
                    icon="📝"
                )

            ],

            "Maintenance": [

                st.Page(
                    "pages/7_Preventive_Maintenance.py",
                    title="My Maintenance Tasks",
                    icon="🗓️"
                )

            ]

        }


    else:

        st.error(
            "Invalid role."
        )

        st.stop()


    # =================================================
    # SIDEBAR USER INFORMATION
    # =================================================

    with st.sidebar:

        st.markdown("---")

        st.write(
            f"👤 **User:** {username}"
        )

        st.write(
            f"🔑 **Role:** {role}"
        )

        st.markdown("---")

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False

            st.session_state.username = ""

            st.session_state.role = ""

            st.rerun()


    # =================================================
    # START NAVIGATION
    # =================================================

    pg = st.navigation(
        pages
    )

    pg.run()