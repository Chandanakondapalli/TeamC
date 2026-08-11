import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Agentic FacilityOps AI Platform",
    page_icon="🏭",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_role" not in st.session_state:
    st.session_state.user_role = None

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "username" not in st.session_state:
    st.session_state.username = None


# ============================================================
# PAGE DEFINITIONS
# ============================================================

login = st.Page(
    "pages/0_🔐_Login.py",
    title="Login",
    icon="🔐"
)

home = st.Page(
    "pages/Home.py",
    title="Home",
    icon="🏠"
)

dashboard = st.Page(
    "pages/1_📈_Dashboard.py",
    title="Dashboard",
    icon="📈"
)

data_analysis = st.Page(
    "pages/2_📊_Data_Analysis.py",
    title="Data Analysis",
    icon="📊"
)

machine_explorer = st.Page(
    "pages/3_🔍_Machine_Explorer.py",
    title="Machine Explorer",
    icon="🔍"
)

ai_assistant = st.Page(
    "pages/4_🤖_AI_Maintenance_Assistant.py",
    title="AI Maintenance Assistant",
    icon="🤖"
)

work_orders = st.Page(
    "pages/5_📝_Work_Orders.py",
    title="Work Orders",
    icon="📝"
)

preventive_maintenance = st.Page(
    "pages/6_🛠️_Preventive_Maintenance.py",
    title="Preventive Maintenance",
    icon="🛠️"
)


# ============================================================
# LOGOUT FUNCTION
# ============================================================

def logout():

    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.user_name = None
    st.session_state.username = None

    st.rerun()


# ============================================================
# NOT LOGGED IN
# ============================================================

if not st.session_state.authenticated:

    pg = st.navigation(
        [login],
        position="hidden"
    )

    pg.run()


# ============================================================
# LOGGED IN
# ============================================================

else:

    role = st.session_state.user_role


    # --------------------------------------------------------
    # EMPLOYEE ACCESS
    # --------------------------------------------------------

    if role == "Employee":

        allowed_pages = [
            home,
            dashboard,
            data_analysis,
            machine_explorer,
            ai_assistant,
            work_orders,
            preventive_maintenance
        ]


    # --------------------------------------------------------
    # TECHNICIAN ACCESS
    # --------------------------------------------------------

    elif role == "Technician":

        allowed_pages = [
            home,
            machine_explorer,
            work_orders,
            preventive_maintenance
        ]


    # --------------------------------------------------------
    # UNKNOWN ROLE
    # --------------------------------------------------------

    else:

        st.session_state.authenticated = False
        st.session_state.user_role = None

        st.rerun()


    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    pg = st.navigation(
        allowed_pages,
        position="sidebar"
    )


    # --------------------------------------------------------
    # SIDEBAR USER INFO
    # --------------------------------------------------------

    with st.sidebar:

        st.divider()

        st.markdown(
            f"### 👤 {st.session_state.user_name}"
        )

        st.caption(
            f"Role: {st.session_state.user_role}"
        )

        st.write("")

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):
            logout()


    # --------------------------------------------------------
    # RUN SELECTED PAGE
    # --------------------------------------------------------

    pg.run()