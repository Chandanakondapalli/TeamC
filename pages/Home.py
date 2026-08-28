import streamlit as st
import pandas as pd

from utils.ui import page_header, load_css
from utils.auth import require_login


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Agentic AI | Smart Facility Operations",
    page_icon="🏭",
    layout="wide"
)


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
# LOAD DATASET
# ============================================================

@st.cache_data
def load_data():

    return pd.read_csv(
        "data/ai4i2020.csv"
    )


df = load_data()


# ============================================================
# PAGE HEADER
# ============================================================

page_header(
    "🏭",
    "Agentic AI for Smart Facility Operations and Optimization",
    "AI-powered predictive maintenance and intelligent facility operations."
)


# ============================================================
# WELCOME
# ============================================================

with st.container(border=True):

    st.markdown("## 👋 Welcome back")

    st.markdown(
        f"### {user_name}"
    )

    st.caption(
        f"Logged in as {user_role}"
    )

    st.write(
        "Turn industrial machine data into actionable maintenance "
        "intelligence — from monitoring and failure analysis to "
        "AI recommendations and work-order execution."
    )


# ============================================================
# QUICK ACTIONS
# ============================================================

st.markdown("### 🚀 Quick Actions")


col1, col2, col3 = st.columns(3)


with col1:

    if st.button(
        "📊 Open Dashboard",
        type="primary",
        use_container_width=True
    ):

        st.switch_page(
            "pages/1_📈_Dashboard.py"
        )


with col2:

    if st.button(
        "🤖 AI Maintenance",
        use_container_width=True
    ):

        st.switch_page(
            "pages/4_🤖_AI_Maintenance_Assistant.py"
        )


with col3:

    if st.button(
        "🔍 Machine Explorer",
        use_container_width=True
    ):

        st.switch_page(
            "pages/3_🔍_Machine_Explorer.py"
        )


# ============================================================
# PLATFORM STATUS
# ============================================================

st.markdown("### 🟢 Platform Status")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🏭 Machines",
        f"{len(df):,}"
    )


with col2:

    failures = int(
        df["Machine failure"].sum()
    )

    st.metric(
        "⚠️ Failure Events",
        f"{failures:,}"
    )


with col3:

    failure_rate = (
        failures / len(df) * 100
        if len(df) > 0
        else 0
    )

    st.metric(
        "📈 Failure Rate",
        f"{failure_rate:.2f}%"
    )


with col4:

    st.metric(
        "🔎 Failure Modes",
        "5"
    )


st.divider()


# ============================================================
# WHAT THE PLATFORM DOES
# ============================================================

st.markdown("## 🧠 What Does This Platform Do?")

st.caption(
    "A connected workflow for intelligent predictive maintenance."
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    with st.container(border=True):

        st.markdown("### 📡 Monitor")

        st.write(
            "Analyze machine operating parameters and "
            "sensor readings."
        )


with col2:

    with st.container(border=True):

        st.markdown("### 🔍 Detect")

        st.write(
            "Identify abnormal conditions, failure indicators "
            "and machine risks."
        )


with col3:

    with st.container(border=True):

        st.markdown("### 🤖 Predict")

        st.write(
            "Use engineering analysis and Gemini AI to "
            "assess machine health."
        )


with col4:

    with st.container(border=True):

        st.markdown("### 🛠️ Act")

        st.write(
            "Turn maintenance recommendations into "
            "structured work orders."
        )


# ============================================================
# PLATFORM WORKFLOW
# ============================================================

st.markdown("## ⚙️ Maintenance Intelligence Workflow")

st.caption(
    "From raw machine data to real maintenance execution."
)


workflow = [
    (
        "01",
        "📊",
        "Data Analysis",
        "Explore machine data"
    ),
    (
        "02",
        "📈",
        "Dashboard",
        "Monitor facility KPIs"
    ),
    (
        "03",
        "🔍",
        "Machine Explorer",
        "Inspect machine health"
    ),
    (
        "04",
        "🤖",
        "AI Maintenance",
        "Generate AI assessment"
    ),
    (
        "05",
        "🛠️",
        "Preventive Maintenance",
        "Plan maintenance"
    ),
    (
        "06",
        "📝",
        "Work Orders",
        "Execute maintenance"
    )
]


cols = st.columns(6)


for col, item in zip(
    cols,
    workflow
):

    number, icon, title, description = item

    with col:

        with st.container(border=True):

            st.caption(
                f"STEP {number}"
            )

            st.markdown(
                f"## {icon}"
            )

            st.markdown(
                f"**{title}**"
            )

            st.caption(
                description
            )


# ============================================================
# AI INTELLIGENCE
# ============================================================

st.markdown("## 🤖 AI-Powered Maintenance Intelligence")

st.caption(
    "Convert machine condition data into engineering decisions."
)


col1, col2, col3 = st.columns(3)


with col1:

    with st.container(border=True):

        st.markdown(
            "### 🧠 Machine Health Assessment"
        )

        st.write(
            "Evaluate machine health using sensor parameters, "
            "failure indicators and engineering calculations."
        )

        st.success(
            "Health Score"
        )


with col2:

    with st.container(border=True):

        st.markdown(
            "### ⚠️ Risk & Failure Analysis"
        )

        st.write(
            "Analyze failure conditions, thermal behavior, "
            "tool wear and operational risk."
        )

        st.warning(
            "Risk Detection"
        )


with col3:

    with st.container(border=True):

        st.markdown(
            "### 🔧 Maintenance Recommendations"
        )

        st.write(
            "Generate practical maintenance recommendations "
            "and connect them with work-order execution."
        )

        st.info(
            "AI Recommendations"
        )


# ============================================================
# PLATFORM MODULES
# ============================================================

st.markdown("## 🚀 Explore Platform Modules")

st.caption(
    "Everything required for machine monitoring and maintenance management."
)


modules = [
    (
        "📊",
        "Data Analysis",
        "Explore distributions, relationships, correlations and failure patterns."
    ),
    (
        "📈",
        "Dashboard",
        "Monitor KPIs, machine statistics and facility-level insights."
    ),
    (
        "🔍",
        "Machine Explorer",
        "Search individual machines and inspect their sensor information."
    ),
    (
        "🤖",
        "AI Maintenance Assistant",
        "Generate machine health assessments and maintenance recommendations."
    ),
    (
        "🛠️",
        "Preventive Maintenance",
        "Plan and manage preventive maintenance activities."
    ),
    (
        "📝",
        "Work Orders",
        "Create, assign and track maintenance work orders."
    )
]


for row in range(
    0,
    len(modules),
    3
):

    cols = st.columns(3)

    for col, module in zip(
        cols,
        modules[row:row + 3]
    ):

        icon, title, description = module

        with col:

            with st.container(border=True):

                st.markdown(
                    f"### {icon} {title}"
                )

                st.caption(
                    description
                )


# ============================================================
# WHY IT MATTERS
# ============================================================

st.markdown("## 🎯 Why This Platform?")

col1, col2, col3 = st.columns(3)


with col1:

    with st.container(border=True):

        st.markdown("### ⏱️ Reduce Downtime")

        st.write(
            "Identify potential machine problems earlier "
            "and support proactive maintenance planning."
        )


with col2:

    with st.container(border=True):

        st.markdown("### 📋 Improve Maintenance")

        st.write(
            "Organize recommendations, priorities, technicians "
            "and maintenance activities in one workflow."
        )


with col3:

    with st.container(border=True):

        st.markdown("### 🧠 Support Decisions")

        st.write(
            "Combine machine analytics, engineering metrics "
            "and AI-generated insights for better decisions."
        )


# ============================================================
# FINAL CALL TO ACTION
# ============================================================

st.divider()

with st.container(border=True):

    st.markdown(
        "## 🚀 Ready to explore the facility?"
    )

    st.write(
        "Start by opening the dashboard or select a machine "
        "to generate an AI-powered maintenance assessment."
    )

    col1, col2, col3 = st.columns(
        [1, 1, 1]
    )

    with col1:

        if st.button(
            "📊 Go to Dashboard",
            type="primary",
            use_container_width=True
        ):

            st.switch_page(
                "pages/1_📈_Dashboard.py"
            )

    with col2:

        if st.button(
            "🔍 Explore a Machine",
            use_container_width=True
        ):

            st.switch_page(
                "pages/3_🔍_Machine_Explorer.py"
            )

    with col3:

        if st.button(
            "🤖 Ask AI",
            use_container_width=True
        ):

            st.switch_page(
                "pages/4_🤖_AI_Maintenance_Assistant.py"
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🏭 Agentic AI for Smart Facility Operations and Optimization"
)

st.caption(
    "AI-Powered Industrial Predictive Maintenance • Infosys Springboard Internship"
)