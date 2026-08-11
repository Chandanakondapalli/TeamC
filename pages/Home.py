import streamlit as st

from utils.ui import *
from utils.cards import *
from utils.charts import *
from utils.themes import *
from utils.auth import require_login


# ============================================================
# AUTHENTICATION
# ============================================================

require_login()

load_css()


# ============================================================
# USER INFORMATION
# ============================================================

user_name = st.session_state.get(
    "user_name",
    "Facility User"
)

user_role = st.session_state.get(
    "user_role",
    "Employee"
)


# ============================================================
# WELCOME SECTION
# ============================================================

with st.container(border=True):

    st.markdown(
        f"""
        ## 👋 Welcome, {user_name}

        You are logged in as **{user_role}**.

        Use the navigation menu to access the
        **Agentic FacilityOps AI Platform** modules.
        """
    )


st.write("")


# ============================================================
# ABOUT THE PLATFORM
# ============================================================

st.header("📌 About the Platform")

st.write(
    """
    The **Agentic FacilityOps AI Platform** is an intelligent
    predictive maintenance solution designed to monitor industrial
    machines, analyze sensor data, detect failures, assess
    operational risks, and generate AI-powered maintenance
    recommendations.
    """
)

st.write(
    """
    The platform combines data analytics, visualization,
    machine exploration, artificial intelligence, preventive
    maintenance, and work order management to improve
    maintenance efficiency and reduce unexpected equipment failures.
    """
)

st.divider()


# ============================================================
# PLATFORM WORKFLOW
# ============================================================

# ============================================================
# PLATFORM WORKFLOW
# ============================================================

st.header("🔄 Platform Workflow")

workflow = [
    ("01", "AI4I Dataset", "Industrial machine sensor data"),
    ("02", "Data Analysis", "Explore and analyze machine data"),
    ("03", "Dashboard", "Monitor KPIs and failure insights"),
    ("04", "Machine Explorer", "Inspect individual machine health"),
    ("05", "AI Maintenance", "Generate AI maintenance insights"),
    ("06", "Preventive Maintenance", "Plan scheduled maintenance"),
    ("07", "Work Orders", "Create and manage maintenance work"),
]

# First row
cols = st.columns(4)

for col, (step, title, description) in zip(
    cols,
    workflow[:4]
):

    with col:

        with st.container(border=True):

            st.caption(f"STEP {step}")

            st.subheader(title)

            st.write(description)


st.write("")


# Second row
cols = st.columns(4)

for col, (step, title, description) in zip(
    cols[:3],
    workflow[4:]
):

    with col:

        with st.container(border=True):

            st.caption(f"STEP {step}")

            st.subheader(title)

            st.write(description)


# ============================================================
# PLATFORM MODULES
# ============================================================

st.header("🚀 Platform Modules")

modules = [
    (
        "📊",
        "Data Analysis",
        "Explore machine data, statistics, correlations, "
        "failure patterns and visualizations."
    ),
    (
        "📈",
        "Dashboard",
        "Monitor KPIs, machine failures, distributions "
        "and operational insights."
    ),
    (
        "🔍",
        "Machine Explorer",
        "Search individual machines and inspect sensor "
        "values, health and failure information."
    ),
    (
        "🤖",
        "AI Maintenance Assistant",
        "Generate AI-powered machine health assessments "
        "and maintenance recommendations."
    ),
    (
        "🛠️",
        "Preventive Maintenance",
        "Create, update and manage preventive maintenance "
        "schedules."
    ),
    (
        "📝",
        "Work Orders",
        "Create and manage maintenance work orders, "
        "technicians, priorities and statuses."
    ),
]

for row in range(0, len(modules), 2):

    col1, col2 = st.columns(2)

    for col, module in zip(
        [col1, col2],
        modules[row:row + 2]
    ):

        icon, title, description = module

        with col:

            with st.container(border=True):

                st.markdown(
                    f"### {icon} {title}"
                )

                st.write(description)


st.divider()


# ============================================================
# KEY OBJECTIVES
# ============================================================

st.header("🎯 Project Objectives")

objectives = [
    "Predict machine failures before breakdown.",
    "Improve maintenance planning.",
    "Reduce unexpected operational downtime.",
    "Provide AI-powered maintenance insights.",
    "Support intelligent maintenance decision making.",
    "Centralize work order and preventive maintenance management.",
]

for objective in objectives:

    st.markdown(
        f"✓ {objective}"
    )


st.divider()


# ============================================================
# KEY FEATURES
# ============================================================

st.header("⭐ Key Features")

col1, col2, col3 = st.columns(3)

with col1:

    with st.container(border=True):

        st.subheader("🏭 Machine Monitoring")

        st.write(
            "Monitor machine operating parameters, "
            "health status and failure indicators."
        )

with col2:

    with st.container(border=True):

        st.subheader("🤖 AI Intelligence")

        st.write(
            "Generate machine health assessments and "
            "maintenance recommendations using Gemini AI."
        )

with col3:

    with st.container(border=True):

        st.subheader("📝 Maintenance Management")

        st.write(
            "Manage preventive schedules and maintenance "
            "work orders from one platform."
        )


st.divider()


# ============================================================
# TECHNOLOGY STACK
# ============================================================

st.header("🛠️ Technology Stack")

col1, col2, col3 = st.columns(3)

with col1:

    with st.container(border=True):

        st.subheader("Frontend")

        st.write("• Streamlit")
        st.write("• HTML")
        st.write("• CSS")


with col2:

    with st.container(border=True):

        st.subheader("Data & Backend")

        st.write("• Python")
        st.write("• Pandas")
        st.write("• NumPy")
        st.write("• SQLite")


with col3:

    with st.container(border=True):

        st.subheader("AI & Visualization")

        st.write("• Gemini AI")
        st.write("• Matplotlib")
        st.write("• Seaborn")
        st.write("• ReportLab")


st.divider()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="text-align:center; padding:20px;">

    <h4>Agentic FacilityOps AI Platform</h4>

    <p>
    AI-Powered Industrial Predictive Maintenance
    </p>

    <p>
    Developed for Infosys Springboard Internship
    </p>

    </div>
    """,
    unsafe_allow_html=True
)