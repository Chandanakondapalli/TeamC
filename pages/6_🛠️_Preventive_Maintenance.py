import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime
from utils.database import *
from utils.ui import *
from utils.themes import *
from utils.ai_report import generate_preventive_recommendation
from utils.auth import require_login, hide_login_from_sidebar

require_login()
hide_login_from_sidebar()

# ---------------------------------------------------------
# Setup & Data Loading
# ---------------------------------------------------------
init_db()
create_users_table()
seed_users()

DEFAULT_CHECKLIST = [
    "Inspect belts", "Lubricate bearings", "Clean filters",
    "Check motor temperature", "Tighten bolts", "Safety inspection"
]

@st.cache_data
def load_data():
    file_path = "data/ai4i2020.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame()

machine_df = load_data()

st.set_page_config(page_title="Preventive Maintenance", page_icon="🛠️", layout="wide")
load_css()

page_header("🛠️", "Preventive Maintenance", "Create schedules, manage assignments, and monitor activities.")

# --- Global KPIs ---
kpis = get_preventive_kpis()
c1, c2, c3, c4 = st.columns(4)
c1.metric("📅 Total Schedules", kpis["Total"])
c2.metric("⏳ Upcoming", kpis["Upcoming"])
c3.metric("⚠️ Overdue", kpis["Overdue"])
c4.metric("✅ Completed", kpis["Completed"])

tab1, tab2, tab3, tab4 = st.tabs([
    "➕ Create Schedule",
    "📋 Manage Schedules",
    "📅 Tracking & Calendar",
    "🤖 AI Recommendations"
])

# ==========================================
# TAB 1: CREATE SCHEDULE (With ALL Placeholders)
# ==========================================
with tab1:
    st.subheader("➕ Create Preventive Maintenance Schedule")
    
    # 1. Machine ID (OUTSIDE form for reactivity)
    machine_id = st.selectbox(
        "Select Machine",
        options=[""] + sorted(machine_df["Product ID"].unique().tolist()),
        index=0,
        format_func=lambda x: "Choose a Machine ID..." if x == "" else x,
        key="pm_create_select"
    )

    machine_type_val = ""
    if machine_id != "":
        machine_row = machine_df[machine_df["Product ID"] == machine_id].iloc[0]
        machine_type_val = str(machine_row["Type"])
        st.info(f"**Asset Details:** ID: {machine_id} | Type: {machine_type_val} | Wear: {machine_row['Tool wear [min]']} min")

    with st.form("schedule_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("Machine Type", value=machine_type_val, disabled=True)
        with col2:
            # 2. Activity Placeholder
            maintenance_type = st.selectbox(
                "Maintenance Activity", 
                options=["", "Preventive Inspection", "Lubrication", "Calibration", "Cleaning", "Safety Inspection"],
                format_func=lambda x: "Select Type..." if x == "" else x
            )
        with col3:
            # 3. Frequency Placeholder
            frequency = st.selectbox(
                "Frequency", 
                options=["", "Weekly", "Monthly", "Quarterly", "Yearly"],
                format_func=lambda x: "Select Frequency..." if x == "" else x
            )

        col1, col2, col3 = st.columns(3)
        with col1:
            # 4. Technician Placeholder
            technician = st.selectbox(
                "Assign Staff", 
                options=["", "John Smith", "Sarah Wilson", "Michael Brown", "David Lee"],
                format_func=lambda x: "Assign Personnel..." if x == "" else x
            )
        with col2:
            # 5. Priority Placeholder
            priority = st.selectbox(
                "Priority", 
                options=["", "Low", "Medium", "High"],
                format_func=lambda x: "Set Priority..." if x == "" else x
            )
        with col3:
            start_date = st.date_input("Start Date", value=date.today())

        if st.form_submit_button("✅ Create Schedule", type="primary", use_container_width=True):
            if "" in [machine_id, maintenance_type, frequency, technician, priority]:
                st.error("⚠️ All fields are required. Please select values for all dropdowns.")
            else:
                insert_preventive_schedule(machine_id, machine_type_val, maintenance_type, frequency, start_date, technician, priority)
                st.success("✅ Schedule created!")
                st.rerun()

# ==========================================
# TAB 2: MANAGE SCHEDULES (With Search & Delete)
# ==========================================
with tab2:
    st.subheader("📋 Existing Maintenance Schedules")
    
    search_q = st.text_input("🔍 Search by Machine ID or Technician", placeholder="Type to filter list...")
    
    schedule_df = get_all_preventive_schedules()
    if not schedule_df.empty:
        if search_q:
            schedule_df = schedule_df[schedule_df['machine_id'].str.contains(search_q, case=False) | schedule_df['technician'].str.contains(search_q, case=False)]

        for _, row in schedule_df.iterrows():
            with st.container(border=True):
                c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 0.5])
                c1.write(f"**Asset:** {row['machine_id']}")
                c2.write(f"**Task:** {row['maintenance_type']}")
                c3.write(f"**Due:** {row['next_due_date']}")
                c4.write(f"**Status:** {row['status']}")
                
                # --- DELETE BUTTON ---
                if c5.button("🗑️", key=f"del_{row['schedule_id']}", help="Delete this schedule"):
                    delete_preventive_schedule(row['schedule_id'])
                    st.rerun()

                # --- UPDATE STATUS ---
                new_status = st.selectbox("Update Status", ["Upcoming", "In Progress", "Completed"], 
                                         index=["Upcoming", "In Progress", "Completed"].index(row["status"]), 
                                         key=f"st_{row['schedule_id']}")
                if new_status != row["status"]:
                    update_schedule_status(row["schedule_id"], new_status)
                    if new_status == "Completed":
                        add_maintenance_history(row["schedule_id"], row["machine_id"], row["technician"])
                    st.rerun()

                # --- GENERATE WORK ORDER (Restore) ---
                with st.expander("📝 Generate Work Order"):
                    if row.get("work_order_created", 0) == 0:
                        if st.button("Generate Work Order", key=f"wo_{row['schedule_id']}", type="primary"):
                            insert_work_order(machine_id=row["machine_id"], machine_type=row["machine_type"], priority=row["priority"],
                                             maintenance_type=row["maintenance_type"], technician=row["technician"], due_date=row["next_due_date"],
                                             estimated_cost=2500.0, estimated_time="2 Hours", description=f"PM: {row['maintenance_type']}")
                            mark_work_order_created(row["schedule_id"])
                            st.success("✅ Work Order Sent to Module 5")
                            st.rerun()
                    else:
                        st.success("✅ Work Order Already Active")

                # --- CHECKLIST (Restore) ---
                with st.expander("📋 Maintenance Checklist"):
                    checks = []
                    for task in DEFAULT_CHECKLIST:
                        if st.checkbox(task, key=f"chk_{row['schedule_id']}_{task}"):
                            checks.append(task)
                    if st.button("Mark as Done", key=f"comp_{row['schedule_id']}"):
                        if len(checks) < len(DEFAULT_CHECKLIST):
                            st.warning("Complete all steps first.")
                        else:
                            update_schedule_status(row["schedule_id"], "Completed")
                            add_maintenance_history(row["schedule_id"], row["machine_id"], row["technician"])
                            st.rerun()

# ==========================================
# TAB 3: TRACKING & CALENDAR (Restore Overdue/Upcoming)
# ==========================================
with tab3:
    st.subheader("📅 Maintenance Calendar")
    cal_df = get_all_preventive_schedules()
    if not cal_df.empty:
        cal_df['start_date'] = pd.to_datetime(cal_df['start_date'])
        cal_df['next_due_date'] = pd.to_datetime(cal_df['next_due_date'])
        fig = px.timeline(cal_df, x_start="start_date", x_end="next_due_date", y="machine_id", color="priority",
                         color_discrete_map={"High": "#EF4444", "Medium": "#F59E0B", "Low": "#22C55E"})
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)

    
    st.subheader("⏳ Upcoming Tasks")
    st.dataframe(get_upcoming_maintenance(), use_container_width=True, hide_index=True)
    
    st.subheader("⚠️ Overdue Tasks")
    st.dataframe(get_overdue_maintenance(), use_container_width=True, hide_index=True)

    st.subheader("📜 Maintenance History")
    st.dataframe(get_maintenance_history(), use_container_width=True, hide_index=True)

# ==========================================
# TAB 4: AI RECOMMENDATIONS (Restore)
# ==========================================
# ... (Keep existing imports at the top)

with tab4:
    st.subheader("🤖 AI-Based Preventive Maintenance Recommendations")
    st.info("AI analyzes real-time sensor data and historical wear patterns to suggest optimized maintenance actions.")

    # 1. Select Asset for Analysis
    machine_id_ai = st.selectbox(
        "Select Asset for AI Audit", 
        options=[""] + sorted(machine_df["Product ID"].unique().tolist()),
        index=0,
        format_func=lambda x: "Choose an Asset to Analyze..." if x == "" else x,
        key="pm_ai_audit_select"
    )

    if st.button("🔍 Run AI Diagnostics", type="primary", use_container_width=True):
        if machine_id_ai == "":
            st.warning("⚠ Please select a machine first.")
        else:
            # Fetch specific machine row
            m_data = machine_df[machine_df["Product ID"] == machine_id_ai].iloc[0]
            
            with st.spinner(f"🤖 AI is analyzing {machine_id_ai} health patterns..."):
                # Call the AI Utility
                # Ensure generate_preventive_recommendation returns:
                # { 'recommendation': 'FULL_MARKDOWN_TEXT', 'description': 'SHORT_SUMMARY_TEXT' }
                res = generate_preventive_recommendation(m_data)
                
                # Save results to Session State to persist through button clicks
                st.session_state["pm_ai_report"] = res['recommendation']
                st.session_state["pm_ai_description"] = res['description']
                st.session_state["pm_ai_machine"] = machine_id_ai
                st.session_state["pm_ai_type"] = str(m_data["Type"])

    # 2. Display the Results & Action Button
    if "pm_ai_report" in st.session_state:
        # Check if the currently displayed report matches the selected machine
        if st.session_state["pm_ai_machine"] == machine_id_ai:
            
            with st.container(border=True):
                st.markdown("### 📋 AI Engineering Recommendation")
                st.markdown(st.session_state["pm_ai_report"])
                
                st.divider()
                st.subheader("⚡ Quick Action")
                st.write(f"Convert this AI recommendation into a formal Work Order for **{machine_id_ai}**.")
                
                # --- THE APPLY BUTTON ---
                if st.button("🚀 Apply Recommendation & Create Work Order", use_container_width=True, type="primary"):
                    
                    # Pull the clean description we saved earlier
                    # This avoids the "========" header issues
                    detailed_desc = st.session_state.get("pm_ai_description", "Maintenance required based on AI sensor analysis.")

                    # A. Create the Work Order in Module 5
                    new_wo_id = insert_work_order(
                        machine_id=st.session_state["pm_ai_machine"],
                        machine_type=st.session_state["pm_ai_type"],
                        priority="High", 
                        maintenance_type="Predictive",
                        technician="AI Assigned Specialist",
                        due_date=date.today().strftime("%Y-%m-%d"),
                        estimated_cost=5000.0,
                        estimated_time="3 Hours",
                        # PASSING THE CLEAN DESCRIPTION HERE:
                        description=f"AI GENERATED: {detailed_desc}"
                    )

                    # B. Also create a log in the Preventive Schedules table
                    insert_preventive_schedule(
                        machine_id=st.session_state["pm_ai_machine"],
                        machine_type=st.session_state["pm_ai_type"],
                        maintenance_type="AI Recommended Fix",
                        frequency="One-Time",
                        start_date=date.today(),
                        technician="AI Assigned Specialist",
                        priority="High"
                    )
                    
                    st.success(f"✅ Success! Work Order **{new_wo_id}** created with full AI diagnostics.")
                    st.balloons()
                    
                    # Clean up session state so the button disappears after successful creation
                    del st.session_state["pm_ai_report"]
                    st.info("Navigate to the **Work Orders** page to view the details.")
        else:
            st.caption("Machine selection changed. Run diagnostics again to see updated report.")