import streamlit as st
import pandas as pd


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Predictive Maintenance System",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOGIN CHECK
# =========================================================

if not st.session_state.get("logged_in", False):
    st.warning("🔒 Please login to access the system.")
    st.stop()


# =========================================================
# USER DETAILS
# =========================================================

username = st.session_state.get("username", "")
role = st.session_state.get("role", "")

username = str(username).strip()
role = str(role).strip()


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}


/* ================= HERO ================= */

.hero {
    background: linear-gradient(135deg, #0f172a, #1e3a8a, #2563eb);
    padding: 42px 45px;
    border-radius: 22px;
    margin-bottom: 28px;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.18);
}

.hero-icon {
    font-size: 42px;
    margin-bottom: 8px;
}

.hero-title {
    color: white;
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero-subtitle {
    color: #dbeafe;
    font-size: 18px;
    line-height: 1.6;
    margin-bottom: 18px;
}

.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    color: #e0f2fe;
    padding: 8px 15px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
}


/* ================= SECTION ================= */

.section-title {
    font-size: 25px;
    font-weight: 750;
    color: #0f172a;
    margin-top: 28px;
    margin-bottom: 5px;
}

.section-description {
    color: #64748b;
    font-size: 15px;
    margin-bottom: 18px;
}


/* ================= ACCOUNT CARDS ================= */

.account-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 22px;
    min-height: 135px;
    box-shadow: 0 4px 14px rgba(15,23,42,0.06);
}

.account-label {
    color: #64748b;
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.account-value {
    color: #0f172a;
    font-size: 22px;
    font-weight: 700;
}

.access-badge {
    display: inline-block;
    background: #dcfce7;
    color: #166534;
    padding: 7px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
}


/* ================= STATUS ================= */

.status-card {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 16px;
    padding: 20px 24px;
    margin-top: 20px;
    margin-bottom: 30px;
}

.status-title {
    color: #166534;
    font-size: 18px;
    font-weight: 750;
    margin-bottom: 6px;
}

.status-text {
    color: #475569;
    font-size: 14px;
}


/* ================= KPI ================= */

.kpi-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 22px;
    min-height: 145px;
    box-shadow: 0 4px 14px rgba(15,23,42,0.06);
}

.kpi-label {
    color: #64748b;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 12px;
}

.kpi-value {
    color: #0f172a;
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 5px;
}

.kpi-small {
    color: #64748b;
    font-size: 13px;
}


/* ================= MODULE CARDS ================= */

.module-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 24px;
    min-height: 190px;
    margin-bottom: 20px;
    box-shadow: 0 4px 14px rgba(15,23,42,0.06);
    transition: 0.2s;
}

.module-card:hover {
    border-color: #93c5fd;
    box-shadow: 0 8px 20px rgba(37,99,235,0.10);
}

.module-icon {
    font-size: 30px;
    margin-bottom: 12px;
}

.module-title {
    color: #0f172a;
    font-size: 18px;
    font-weight: 750;
    margin-bottom: 8px;
}

.module-description {
    color: #64748b;
    font-size: 14px;
    line-height: 1.6;
}


/* ================= FOOTER ================= */

.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 13px;
    padding: 25px 0 5px 0;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# HERO SECTION
# =========================================================

st.markdown(
    """
<div class="hero">
<div class="hero-icon">🏭</div>
<div class="hero-title">Predictive Maintenance System</div>
<div class="hero-subtitle">
AI-powered platform for monitoring machines,
predicting failures, and managing maintenance
operations efficiently.
</div>
<div class="hero-badge">
🟢 SYSTEM ONLINE &nbsp; | &nbsp; AI-POWERED MAINTENANCE OPERATIONS
</div>
</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# ACCOUNT INFORMATION
# =========================================================

st.markdown(
    """
<div class="section-title">👤 Account Information</div>
<div class="section-description">
Your current system account and access information.
</div>
""",
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)


# USER
with col1:
    st.markdown(
        f"""
<div class="account-card">
<div class="account-label">👤 Logged-in User</div>
<div class="account-value">{username}</div>
</div>
""",
        unsafe_allow_html=True
    )


# ROLE
with col2:
    st.markdown(
        f"""
<div class="account-card">
<div class="account-label">🔑 System Role</div>
<div class="account-value">{role}</div>
</div>
""",
        unsafe_allow_html=True
    )


# ACCESS
with col3:

    if role.lower() == "admin":
        access_text = "🛡️ Full System Access"
    else:
        access_text = "🛡️ Technician Access"

    st.markdown(
        f"""
<div class="account-card">
<div class="account-label">🛡️ Access Level</div>
<br>
<span class="access-badge">{access_text}</span>
</div>
""",
        unsafe_allow_html=True
    )


# =========================================================
# SYSTEM STATUS
# =========================================================

st.markdown(
    """
<div class="status-card">
<div class="status-title">🟢 System Operational</div>
<div class="status-text">
Predictive maintenance monitoring, machine analytics,
and work order management services are currently available.
</div>
</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# ADMIN HOME
# =========================================================

if role.lower() == "admin":

    # -----------------------------------------------------
    # OPERATIONS OVERVIEW
    # -----------------------------------------------------

    st.markdown(
        """
<div class="section-title">📊 Operations Overview</div>
<div class="section-description">
Monitor your complete predictive maintenance operation
from one central workspace.
</div>
""",
        unsafe_allow_html=True
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:
        st.markdown(
            """
<div class="kpi-card">
<div class="kpi-label">🏭 TOTAL MACHINES</div>
<div class="kpi-value">10,000</div>
<div class="kpi-small">↑ Fleet monitored</div>
</div>
""",
            unsafe_allow_html=True
        )


    with col2:
        st.markdown(
            """
<div class="kpi-card">
<div class="kpi-label">⚠️ MACHINE FAILURES</div>
<div class="kpi-value">339</div>
<div class="kpi-small">Action required</div>
</div>
""",
            unsafe_allow_html=True
        )


    with col3:
        st.markdown(
            """
<div class="kpi-card">
<div class="kpi-label">📋 WORK ORDERS</div>
<div class="kpi-value">145</div>
<div class="kpi-small">Maintenance operations</div>
</div>
""",
            unsafe_allow_html=True
        )


    with col4:
        st.markdown(
            """
<div class="kpi-card">
<div class="kpi-label">👨‍🔧 TECHNICIANS</div>
<div class="kpi-value">4</div>
<div class="kpi-small">Active technicians</div>
</div>
""",
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # MAINTENANCE OPERATIONS
    # -----------------------------------------------------

    st.markdown(
        """
<div class="section-title">🚀 Maintenance Operations</div>
<div class="section-description">
Access system modules and manage the complete maintenance lifecycle.
</div>
""",
        unsafe_allow_html=True
    )


    # ROW 1

    col1, col2, col3 = st.columns(3)


    with col1:
        st.markdown(
            """
<div class="module-card">
<div class="module-icon">📊</div>
<div class="module-title">Exploratory Data Analysis</div>
<div class="module-description">
Analyze machine sensor data, identify patterns,
and understand failure-related factors.
</div>
</div>
""",
            unsafe_allow_html=True
        )


    with col2:
        st.markdown(
            """
<div class="module-card">
<div class="module-icon">📈</div>
<div class="module-title">Maintenance Dashboard</div>
<div class="module-description">
Monitor machine health, failures, KPIs,
and maintenance performance.
</div>
</div>
""",
            unsafe_allow_html=True
        )


    with col3:
        st.markdown(
            """
<div class="module-card">
<div class="module-icon">🏭</div>
<div class="module-title">Machine Explorer</div>
<div class="module-description">
Search machines, inspect sensor values,
and analyze machine health.
</div>
</div>
""",
            unsafe_allow_html=True
        )


    # ROW 2

    col1, col2, col3 = st.columns(3)


    with col1:
        st.markdown(
            """
<div class="module-card">
<div class="module-icon">🤖</div>
<div class="module-title">AI Maintenance Assistant</div>
<div class="module-description">
Generate AI-powered maintenance recommendations
and machine analysis.
</div>
</div>
""",
            unsafe_allow_html=True
        )


    with col2:
        st.markdown(
            """
<div class="module-card">
<div class="module-icon">📝</div>
<div class="module-title">Work Order Creation</div>
<div class="module-description">
Create maintenance work orders,
assign technicians, and set priorities.
</div>
</div>
""",
            unsafe_allow_html=True
        )


    with col3:
        st.markdown(
            """
<div class="module-card">
<div class="module-icon">📋</div>
<div class="module-title">Work Order Management</div>
<div class="module-description">
Search, update, monitor, and manage
all maintenance work orders.
</div>
</div>
""",
            unsafe_allow_html=True
        )


    # ROW 3

    col1, col2, col3 = st.columns(3)


    with col1:
        st.markdown(
            """
<div class="module-card">
<div class="module-icon">🗓️</div>
<div class="module-title">Preventive Maintenance</div>
<div class="module-description">
Create maintenance schedules, assign technicians,
track overdue tasks, and monitor maintenance.
</div>
</div>
""",
            unsafe_allow_html=True
        )


# =========================================================
# TECHNICIAN HOME
# =========================================================

elif role.lower() == "technician":

    # -----------------------------------------------------
    # PERSONAL OVERVIEW
    # -----------------------------------------------------

    st.markdown(
        """
<div class="section-title">🧑‍🔧 My Maintenance Overview</div>
<div class="section-description">
View your assigned maintenance activities and work orders.
</div>
""",
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(3)


    with col1:
        st.markdown(
            """
<div class="kpi-card">
<div class="kpi-label">📝 MY WORK ORDERS</div>
<div class="kpi-value">12</div>
<div class="kpi-small">Assigned to you</div>
</div>
""",
            unsafe_allow_html=True
        )


    with col2:
        st.markdown(
            """
<div class="kpi-card">
<div class="kpi-label">⏳ PENDING TASKS</div>
<div class="kpi-value">5</div>
<div class="kpi-small">Require attention</div>
</div>
""",
            unsafe_allow_html=True
        )


    with col3:
        st.markdown(
            """
<div class="kpi-card">
<div class="kpi-label">✅ COMPLETED TASKS</div>
<div class="kpi-value">7</div>
<div class="kpi-small">Successfully completed</div>
</div>
""",
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # TECHNICIAN MODULES
    # -----------------------------------------------------

    st.markdown(
        """
<div class="section-title">🛠️ My Maintenance Modules</div>
<div class="section-description">
Tools available for your technician account.
</div>
""",
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(3)


    with col1:
        st.markdown(
            """
<div class="module-card">
<div class="module-icon">🏭</div>
<div class="module-title">Machine Explorer</div>
<div class="module-description">
View machine information, sensor readings,
and machine health conditions.
</div>
</div>
""",
            unsafe_allow_html=True
        )


    with col2:
        st.markdown(
            """
<div class="module-card">
<div class="module-icon">🤖</div>
<div class="module-title">AI Maintenance Assistant</div>
<div class="module-description">
Ask AI questions about machines and
receive maintenance guidance.
</div>
</div>
""",
            unsafe_allow_html=True
        )


    with col3:
        st.markdown(
            """
<div class="module-card">
<div class="module-icon">📋</div>
<div class="module-title">My Work Orders</div>
<div class="module-description">
View and update work orders assigned
specifically to you.
</div>
</div>
""",
            unsafe_allow_html=True
        )


    col1, col2, col3 = st.columns(3)


    with col1:
        st.markdown(
            """
<div class="module-card">
<div class="module-icon">🗓️</div>
<div class="module-title">My Maintenance Tasks</div>
<div class="module-description">
View scheduled maintenance, upcoming tasks,
and overdue maintenance assigned to you.
</div>
</div>
""",
            unsafe_allow_html=True
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
<div class="footer">
🏭 Predictive Maintenance System
&nbsp; • &nbsp;
AI-powered maintenance management
&nbsp; • &nbsp;
Secure Role-Based Access
</div>
""",
    unsafe_allow_html=True
)