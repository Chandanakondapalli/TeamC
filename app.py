import streamlit as st
import pandas as pd
import ollama
from database import init_db
from eda import show_eda

# Import Sub-Modules
from dashboard import show_dashboard
from machine_explorer import show_machine_explorer
from work_orders_hub import show_work_orders_hub
from maintenance import show_maintenance_module

st.set_page_config(page_title="Agentice FacilityOps AI Platform", layout="wide")

# Initialize Database
init_db()

# Initialize Session State Variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "role" not in st.session_state:
    st.session_state.role = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"  # 'login' or 'forgot_password'

# Mock User Database with Roles and Email Verification
if "user_db" not in st.session_state:
    st.session_state.user_db = {
        "admin": {
            "password": "admin123",
            "email": "admin@factory.com",
            "role": "admin",
            "name": "System Administrator"
        },
        "tech": {
            "password": "tech123",
            "email": "tech@factory.com",
            "role": "technician",
            "name": "Field Technician"
        }
    }

# -------------------------------------------------------------
# APPLICATION THEME (SaaS Dark Theme)
# -------------------------------------------------------------
st.markdown("""
<style>
.stApp { 
    background-color: #0f172a !important; 
    color: #f8fafc !important;
}

.stApp p, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, 
.stApp span, .stApp div, .stApp li, .stMarkdown {
    color: #f8fafc !important;
}

section[data-testid="stSidebar"] { 
    background-color: #020617 !important; 
    border-right: 1px solid #1e293b !important;
}
section[data-testid="stSidebar"] * { 
    color: #f8fafc !important; 
}

.sidebar-status-card { 
    padding: 14px; 
    border-radius: 10px; 
    margin-top: 10px; 
    margin-bottom: 15px; 
    font-weight: 600; 
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.35); 
}
.status-healthy { 
    background: linear-gradient(135deg, #065f46 0%, #047857 100%); 
    color: #ffffff !important; 
    border-left: 5px solid #10b981; 
}
.status-warning { 
    background: linear-gradient(135deg, #78350f 0%, #92400e 100%); 
    color: #ffffff !important; 
    border-left: 5px solid #f59e0b; 
}
.status-danger { 
    background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%); 
    color: #ffffff !important; 
    border-left: 5px solid #ef4444; 
}

div[data-testid="metric-container"] { 
    background: #1e293b !important; 
    border-radius: 12px; 
    padding: 18px; 
    border: 1px solid #334155 !important;
    box-shadow: 0px 4px 16px rgba(0, 0, 0, 0.25);
    border-left: 5px solid #06b6d4 !important; 
}
div[data-testid="metric-container"] * { color: #f8fafc !important; }
div[data-testid="stMetricValue"] {
    font-weight: 800 !important;
    font-size: 2.1rem !important;
    color: #38bdf8 !important;
}

div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
    background-color: #1e293b !important;
    color: #ffffff !important;
    border: 1px solid #475569 !important;
    border-radius: 8px !important;
}
div[data-baseweb="select"] * { color: #ffffff !important; }
ul[role="listbox"] { background-color: #1e293b !important; }
li[role="option"] { color: #ffffff !important; }
div[role="radiogroup"] label * { color: #ffffff !important; }

div[data-testid="stTable"], div[data-testid="stDataFrame"] {
    background-color: #1e293b !important;
    border-radius: 10px !important;
    border: 1px solid #334155 !important;
    padding: 8px !important;
}
.stDataFrame * { color: #ffffff !important; }

.stButton>button { 
    background: linear-gradient(90deg, #2563eb 0%, #06b6d4 100%) !important; 
    color: #ffffff !important; 
    border-radius: 8px; 
    height: 44px; 
    font-weight: 700; 
    border: none; 
    box-shadow: 0px 4px 12px rgba(37, 99, 235, 0.35);
}
.stButton>button:hover { 
    background: linear-gradient(90deg, #1d4ed8 0%, #0891b2 100%) !important; 
    box-shadow: 0px 6px 16px rgba(37, 99, 235, 0.5);
}

.stAlert {
    background-color: #1e293b !important;
    color: #ffffff !important;
    border: 1px solid #334155 !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# LOGIN & PASSWORD RESET PAGE
# -------------------------------------------------------------
def show_auth_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Standard Login Screen
        if st.session_state.auth_mode == "login":
            st.markdown("""
                <div style="text-align: center; margin-top: 40px; margin-bottom: 25px;">
                    <h1 style="color: #38bdf8 !important; margin: 0;">⚙️ AI4I Maintenance Hub</h1>
                    <p style="color: #94a3b8 !important; margin-top: 6px;">Sign in to access your dashboard</p>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("login_form"):
                username = st.text_input("Username").strip().lower()
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("🔐 Sign In", use_container_width=True)

                if submit:
                    users = st.session_state.user_db
                    if username in users and users[username]["password"] == password:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.role = users[username]["role"]
                        st.session_state.user_name = users[username]["name"]
                        st.success(f"Welcome back, {users[username]['name']}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid Username or Password")
            
            if st.button("🔑 Forgot Password?", use_container_width=True):
                st.session_state.auth_mode = "forgot_password"
                st.rerun()

        # Forgot / Reset Password Screen
        elif st.session_state.auth_mode == "forgot_password":
            st.markdown("""
                <div style="text-align: center; margin-top: 40px; margin-bottom: 25px;">
                    <h1 style="color: #38bdf8 !important; margin: 0;">🔑 Reset Password</h1>
                    <p style="color: #94a3b8 !important; margin-top: 6px;">Verify your registered email to reset your key</p>
                </div>
            """, unsafe_allow_html=True)

            with st.form("reset_form"):
                username = st.text_input("Username").strip().lower()
                email = st.text_input("Registered Email").strip().lower()
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm New Password", type="password")
                reset_submit = st.form_submit_button("🔄 Update Password", use_container_width=True)

                if reset_submit:
                    users = st.session_state.user_db
                    if username not in users:
                        st.error("❌ User not found.")
                    elif users[username]["email"] != email:
                        st.error("❌ Email address does not match our records.")
                    elif new_password == "":
                        st.warning("⚠️ New password cannot be empty.")
                    elif new_password != confirm_password:
                        st.error("❌ Password confirmation does not match.")
                    else:
                        st.session_state.user_db[username]["password"] = new_password
                        st.success("✅ Password updated successfully! Please log in.")
                        st.session_state.auth_mode = "login"
                        st.rerun()

            if st.button("⬅️ Back to Sign In", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()

# Gatekeeper
if not st.session_state.authenticated:
    show_auth_page()
    st.stop()

# Load Dataset
@st.cache_data
def load_data():
    return pd.read_csv("ai4i2020.csv")

df = load_data()

# Initialize Session State
if "selected_machine" not in st.session_state:
    st.session_state.selected_machine = None
if "ai_report" not in st.session_state:
    st.session_state.ai_report = None
if "ai_report_product_id" not in st.session_state:
    st.session_state.ai_report_product_id = None

# Streaming AI Generator for AI Predictive Diagnostic
def stream_ai_report(row):
    prompt = f"""
You are an Industrial Predictive Maintenance Expert.
Analyze this industrial machine:
Product ID: {row['Product ID']}
Machine Type: {row['Type']}
Air Temp: {row['Air temperature [K]']} K, Process Temp: {row['Process temperature [K]']} K
Speed: {row['Rotational speed [rpm]']} RPM, Torque: {row['Torque [Nm]']} Nm, Tool Wear: {row['Tool wear [min]']} min
Failure Flags: TWF={row['TWF']}, HDF={row['HDF']}, PWF={row['PWF']}, OSF={row['OSF']}, RNF={row['RNF']}

Provide:
## 1. Machine Health Summary
## 2. Sensor Analysis
## 3. Failure Analysis
## 4. Risk Level
## 5. Maintenance Recommendation
## 6. Priority
## 7. Next Inspection
"""
    try:
        response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}], stream=True)
        for chunk in response:
            yield chunk["message"]["content"]
    except Exception as e:
        yield f"❌ **Ollama Connection Error:**\n\n`{e}`"

# -------------------------------------------------------------
# SIDEBAR & USER PROFILE BADGE
# -------------------------------------------------------------
role_badge_color = "#38bdf8" if st.session_state.role == "admin" else "#f59e0b"
st.sidebar.markdown(f"""
    <div style="background: #1e293b; padding: 12px; border-radius: 10px; border: 1px solid #334155; margin-bottom: 15px;">
        <div style="font-size: 12px; color: #94a3b8 !important;">Logged in as:</div>
        <div style="font-weight: bold; font-size: 15px; color: #ffffff !important;">{st.session_state.user_name}</div>
        <div style="font-size: 11px; margin-top: 4px;">
            Role: <span style="background: {role_badge_color}; color: #0f172a; font-weight: bold; padding: 2px 8px; border-radius: 4px; text-transform: uppercase;">{st.session_state.role}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.user_name = None
    st.rerun()

st.sidebar.markdown("---")

# -------------------------------------------------------------
# ROLE-BASED NAVIGATION ROUTING (EXACT REQUESTED ORDER)
# Dashboard ➔ ED Analysis ➔ Machine Explorer ➔ AI Predictive Diagnostic ➔ Work Orders Hub ➔ Preventive Maintenance
# -------------------------------------------------------------
if st.session_state.role == "admin":
    nav_options = [
        "Dashboard", 
        "ED Analysis",
        "Machine Explorer", 
        "AI Predictive Diagnostic",
        "Work Orders Hub",
        "Preventive Maintenance"
    ]
else:
    nav_options = [
        "Machine Explorer", 
        "Work Orders Hub",
        "Preventive Maintenance"
    ]

page = st.sidebar.radio("Navigation", nav_options)

# Sidebar Data Filters
st.sidebar.markdown("---")
st.sidebar.header("Data Filters")

selected_types = st.sidebar.multiselect("Machine Type", options=sorted(df["Type"].unique()), default=sorted(df["Type"].unique()))
status_option = st.sidebar.radio("⚡ Machine Status", options=["All", "Failure", "Healthy machines"], index=0)

filtered_df = df[df["Type"].isin(selected_types)]
if status_option == "Failure":
    filtered_df = filtered_df[filtered_df["Machine failure"] == 1]
elif status_option == "Healthy machines":
    filtered_df = filtered_df[filtered_df["Machine failure"] == 0]

total_selected = len(filtered_df)
failures_count = int(filtered_df["Machine failure"].sum()) if total_selected > 0 else 0
fail_rate = (failures_count / total_selected * 100) if total_selected > 0 else 0

if status_option == "Failure":
    card_class, status_title, status_desc = "status-danger", "🔴 SHOWING FAILURES", f"{total_selected} failed machine(s) isolated"
elif status_option == "Healthy machines":
    card_class, status_title, status_desc = "status-healthy", "🟢 SHOWING HEALTHY", f"{total_selected} healthy machine(s) isolated"
else:
    if fail_rate > 10:
        card_class, status_title, status_desc = "status-danger", "🔴 HIGH FLEET RISK", f"{failures_count} failure(s) ({fail_rate:.1f}%)"
    elif fail_rate > 0:
        card_class, status_title, status_desc = "status-warning", "🟡 WARNING DETECTED", f"{failures_count} failure(s) in selected fleet"
    else:
        card_class, status_title, status_desc = "status-healthy", "🟢 HEALTHY FLEET", "All selected machines running normally"

st.sidebar.markdown(f"""
    <div class="sidebar-status-card {card_class}">
        <div style="font-size: 11px; text-transform: uppercase;">Filtered Fleet Overview</div>
        <div style="font-size: 15px; font-weight: bold;">{status_title}</div>
        <div style="font-size: 12px;">{status_desc}</div>
    </div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# PAGE ROUTING
# -------------------------------------------------------------
if page == "Dashboard":
    show_dashboard(filtered_df, status_option)

elif page == "ED Analysis":
    show_eda(df)

elif page == "Machine Explorer":
    show_machine_explorer(df, filtered_df)

elif page == "AI Predictive Diagnostic":
    st.markdown("""
        <div style="background: #1e293b; padding: 22px; border-radius: 12px; border: 1px solid #334155; text-align: center; margin-bottom: 20px;">
            <h1 style="color: #38bdf8 !important; margin:0;">🤖 Module: AI Predictive Diagnostic</h1>
            <p style="font-size:15px; color: #94a3b8 !important; margin-top:6px;">Run local Llama 3.2 LLM streaming diagnostic models on active machine telemetry.</p>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.selected_machine is None:
        st.warning("⚠️ No machine selected. Please select a machine in **Machine Explorer** first.")
    else:
        row = st.session_state.selected_machine
        st.subheader(f"📌 Active Selected Target: Machine `{row['Product ID']}`")
        if st.button("⚡ Analyze Machine", use_container_width=True):
            with st.status("🔍 Analyzing telemetry via Llama 3.2...", expanded=True) as status_box:
                report_placeholder = st.empty()
                full_report = report_placeholder.write_stream(stream_ai_report(row))
                st.session_state.ai_report = full_report
                st.session_state.ai_report_product_id = row['Product ID']
                status_box.update(label="✅ Diagnostic Analysis Complete!", state="complete", expanded=False)
        elif (st.session_state.ai_report is not None and st.session_state.ai_report_product_id == row['Product ID']):
            st.info(f"💡 Active AI Diagnostic Report for **Machine `{row['Product ID']}`**:")
            st.markdown(st.session_state.ai_report)

elif page == "Work Orders Hub":
    show_work_orders_hub(df)

elif page == "Preventive Maintenance":
    show_maintenance_module(df)