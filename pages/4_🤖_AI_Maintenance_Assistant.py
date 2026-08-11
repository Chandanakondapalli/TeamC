import streamlit as st
import pandas as pd
from utils.ui import *
from utils.themes import *
from utils.database import *
from utils.ai_report import generate_machine_report
from utils.auth import require_login, hide_login_from_sidebar

require_login()
hide_login_from_sidebar()

init_db()
create_users_table()
seed_users()
# ----------------------------------------
# Session State Initialization
# ----------------------------------------
defaults = {
    "show_workorder_form": False,
    "workorder_created": False,
    "open_from_explorer": False,
    "selected_machine_id": "",
    "report_generated": False,
    "report": "",
    "workorder_data": {},
    "last_machine": "",
    "page_mode": "home"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ----------------------------------------
# Page Configuration
# ----------------------------------------
st.set_page_config(
    page_title="AI Maintenance Assistant",
    page_icon="🤖",
    layout="wide"
)

load_css()

page_header(
    "🤖",
    "AI Maintenance Assistant",
    "Generate intelligent machine health assessments and maintenance recommendations using AI."
)

@st.cache_data
def load_data():
    return pd.read_csv("data/ai4i2020.csv")

df = load_data()

# ----------------------------------------
# Machine Selection
# ----------------------------------------
with st.container(border=True):
    st.subheader("Selected Machine")

    if st.session_state.get("open_from_explorer", False):
        machine_id = st.session_state["selected_machine_id"]
        st.info(f"Machine ID : {machine_id}")
    else:
        machine_id = st.selectbox(
            "Machine ID",
            [""] + sorted(df["Product ID"].unique()),
            format_func=lambda x: "Select Product ID..." if x == "" else x,
            index=([""] + sorted(df["Product ID"].unique())).index(st.session_state.get("selected_machine_id", ""))
            if st.session_state.get("selected_machine_id", "") in df["Product ID"].values else 0
        )
        if machine_id == "":
            st.stop()

    machine = df[df["Product ID"] == machine_id].iloc[0]

    # Only reset if machine explicitly changed
    if st.session_state.get("last_machine") != machine_id:
        st.session_state.last_machine = machine_id
        st.session_state.report_generated = False
        st.session_state.report = ""
        st.session_state.workorder_data = {}
        st.session_state.workorder_created = False
        st.session_state.show_workorder_form = False

# Auto-generate report if coming from Explorer
if st.session_state.get("open_from_explorer", False):
    st.session_state.open_from_explorer = False  # Reset flag immediately
    with st.spinner("🤖 AI is analyzing the machine..."):
        result = generate_machine_report(machine)
        st.session_state.report = result["report"]
        st.session_state.workorder_data = result["workorder"]
        st.session_state.report_generated = True

# ----------------------------------------
# Machine Metrics Display
# ----------------------------------------
st.subheader("⚙️ Machine Information")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Machine Type", machine["Type"])
with c2:
    st.metric("RPM", int(machine["Rotational speed [rpm]"]))
with c3:
    st.metric("Torque", f"{machine['Torque [Nm]']} Nm")
with c4:
    st.metric("Tool Wear", f"{machine['Tool wear [min]']} min")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Air Temperature", f"{machine['Air temperature [K]']} K")
with c2:
    st.metric("Process Temperature", f"{machine['Process temperature [K]']} K")
with c3:
    status = "❌ Failed" if machine["Machine failure"] == 1 else "✅ Healthy"
    st.metric("Machine Status", status)

st.divider()

# ----------------------------------------
# AI Analysis & Work Order Section
# ----------------------------------------
st.subheader("🤖 AI Maintenance Analysis")

# Manual generate button if report not yet generated
if not st.session_state.report_generated:
    if st.button("🚀 Generate AI Report", type="primary", use_container_width=True):
        st.session_state.show_workorder_form = False
        st.session_state.workorder_created = False
        with st.spinner("🤖 AI is analyzing the machine..."):
            result = generate_machine_report(machine)
            st.session_state.report = result["report"]
            st.session_state.workorder_data = result["workorder"]
            st.session_state.report_generated = True
            # NEW: Save to global state for the Work Order page to find
            st.session_state["global_ai_description"] = result["workorder"]["description"]
            st.session_state["global_ai_machine"] = machine_id
        st.rerun()

# Display Generated Report
if st.session_state.report_generated:
    st.success("✅ Analysis Completed")

    with st.container(border=True):
        st.markdown(st.session_state.report)
        st.divider()

        if st.session_state.workorder_created:
            st.success(f"✅ Work Order {st.session_state.get('workorder_id', '')} created successfully!")
            if st.button("📋 View Work Orders", use_container_width=True, type="primary"):
                st.switch_page("pages/5_📝_Work_Orders.py")
        else:
            st.markdown("## 📝 Create Work Order")
            st.info("If the AI report recommends maintenance, you can create a work order.")

            if not st.session_state.show_workorder_form:
                if st.button("📝 Create Work Order", use_container_width=True, type="primary"):
                    st.session_state.show_workorder_form = True
                    st.rerun()
            else:
                data = st.session_state.workorder_data

                with st.form("ai_workorder_form"):
                    left, right = st.columns(2)
                    with left:
                        machine_id_val = st.text_input("Machine ID", value=data.get("machine_id", machine["Product ID"]), disabled=True)
                        machine_type_val = st.text_input("Machine Type", value=data.get("machine_type", machine["Type"]), disabled=True)
                        priority_val = st.text_input("Priority", value=data.get("priority", "High"), disabled=True)
                        m_type = data.get("maintenance_type", "Predictive")
                        m_options = ["Preventive", "Predictive", "Corrective"]
                        m_idx = m_options.index(m_type) if m_type in m_options else 0
                        maintenance_type_val = st.selectbox("Maintenance Type", m_options, index=m_idx)

                    with right:
                        technician_val = st.text_input("Technician", value=data.get("technician", "Maintenance Engineer"))
                        due_date_val = st.date_input("Due Date")
                        estimated_cost_val = st.text_input("Estimated Cost", value=data.get("estimated_cost", 10000))
                        estimated_time_val = st.text_input("Estimated Time", value=data.get("estimated_time", "2 Hours"))

                    description_val = st.text_area(
                        "Description",
                        # Use the AI's data directly
                        value=st.session_state.workorder_data.get("description", ""), 
                        height=120
                    )

                    create = st.form_submit_button("✅ Submit Work Order", use_container_width=True, type="primary")

                if create:
                    workorder_id = insert_work_order(
                        machine_id_val,
                        machine_type_val,
                        priority_val,
                        maintenance_type_val,
                        technician_val,
                        str(due_date_val),
                        estimated_cost_val,
                        estimated_time_val,
                        description_val
                    )
                    st.session_state.show_workorder_form = False
                    st.session_state.workorder_created = True
                    st.session_state.workorder_id = workorder_id
                    st.rerun()