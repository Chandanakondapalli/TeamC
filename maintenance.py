import streamlit as st
import pandas as pd
from datetime import date, timedelta, datetime

# Try importing ollama safely
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
def init_maintenance_state():
    if "pm_schedules" not in st.session_state:
        st.session_state["pm_schedules"] = [
            {
                "Schedule ID": "PM-101",
                "Product ID": "M14860",
                "Task Title": "Spindle Lubrication & Alignment",
                "Frequency": "Weekly",
                "Technician": "Rahul",
                "Next Due Date": str(date.today() - timedelta(days=2)),  # Overdue demo
                "Status": "Overdue",
                "Checklist": ["Check Oil Level", "Inspect Alignment", "Clean Filter"],
                "Last Completed": str(date.today() - timedelta(days=9))
            },
            {
                "Schedule ID": "PM-102",
                "Product ID": "L47181",
                "Task Title": "Thermal Sensor Recalibration",
                "Frequency": "Monthly",
                "Technician": "Anita",
                "Next Due Date": str(date.today() + timedelta(days=3)),  # Upcoming demo
                "Status": "Scheduled",
                "Checklist": ["Calibrate Thermocouple", "Inspect Cabling", "Run Diagnostics"],
                "Last Completed": str(date.today() - timedelta(days=27))
            }
        ]

    if "pm_history" not in st.session_state:
        st.session_state["pm_history"] = []

    if "work_orders" not in st.session_state:
        st.session_state["work_orders"] = []


# ==========================================
# AI RECOMMENDATION GENERATOR
# ==========================================
def generate_pm_recommendations(machine_type, tool_wear, failure_status):
    prompt = f"""
You are an expert Industrial Preventive Maintenance Planner. 
Machine Type: {machine_type}
Current Tool Wear: {tool_wear} minutes
Machine Failure Flag: {failure_status}

Provide 3 concise, highly practical preventive maintenance tasks for this machine. 
For each task, specify:
1. Recommended Frequency (e.g., Daily, Weekly, Monthly)
2. Checklist of key inspection steps
3. Critical safety precaution
"""
    if OLLAMA_AVAILABLE:
        try:
            response = ollama.chat(
                model="llama3.2",
                messages=[{"role": "user", "content": prompt}]
            )
            return response["message"]["content"]
        except Exception as e:
            return f"❌ Ollama Error: {e}\n\nMake sure Ollama is running (`ollama serve`)."
    else:
        # Fallback simulation if Ollama isn't installed locally
        return f"""
### 🤖 Recommended Maintenance Plan for {machine_type}-Type Machine

1. **Spindle & Bearing Lubrication**
   - **Frequency:** Weekly
   - **Checklist:** Clean housing, check lubricant levels, measure vibration levels.
   - **Safety:** Lockout/Tagout (LOTO) power before opening bearing guards.

2. **Thermal & Strain Sensor Recalibration**
   - **Frequency:** Monthly (Priority high since Tool Wear is {tool_wear} min)
   - **Checklist:** Test thermocouple responses, check signal wiring, run baseline test cycle.
   - **Safety:** Ensure machine core has cooled below 35°C before inspection.

3. **Drive Belt & Torque Calibration**
   - **Frequency:** Bi-weekly
   - **Checklist:** Inspect belt tension, check drive pulley alignment, inspect torque limits.
   - **Safety:** Wear safety glasses and cut-resistant gloves during tension adjustments.
"""


# ==========================================
# MAIN MODULE DISPLAY FUNCTION
# ==========================================
def show_maintenance_module(df):
    init_maintenance_state()

    st.markdown("""
    <div style=
    padding: 22px;
    border-radius: 16px;
    text-align: center;
    color: white;
    box-shadow: 0px 6px 16px rgba(79, 70, 229, 0.25);
    margin-bottom: 25px;">
    <h1 style="color:white; margin:0;">🗓️Preventive Maintenance & Scheduling</h1>
    <p style="font-size:15px; opacity:0.95; margin-top:8px;">
    Automated scheduling, frequency management, technician checklists, and AI-driven recommendations.
    </p>
    </div>
    """, unsafe_allow_html=True)

    today = date.today()
    schedules = st.session_state["pm_schedules"]

    # Dynamic status calculations
    overdue_count = 0
    upcoming_count = 0

    for s in schedules:
        due_dt = datetime.strptime(s["Next Due Date"], "%Y-%m-%d").date()
        if due_dt < today and s["Status"] != "Completed":
            s["Status"] = "Overdue"
            overdue_count += 1
        elif due_dt >= today and s["Status"] != "Completed":
            s["Status"] = "Scheduled"
            upcoming_count += 1

    # KPI Summary Row
    st.subheader("📊 Maintenance Status Overview")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("📅 Total Schedules", len(schedules))
    k2.metric("⏳ Scheduled Tasks", upcoming_count)
    k3.metric("🚨 Overdue Tasks", overdue_count)
    k4.metric("✅ Completed Logs", len(st.session_state["pm_history"]))

    st.markdown("---")

    # Workflow Tabs
    tab_sched, tab_create, tab_ai, tab_history = st.tabs([
        "📋 Maintenance Calendar & Tasks", 
        "➕ Configure Schedule", 
        "🤖 AI Recommendations", 
        "📜 History Logs"
    ])

    # ------------------------------------
    # TAB 1: CALENDAR & TASK EXECUTION
    # ------------------------------------
    with tab_sched:
        st.subheader("🗓️ Active Schedules & Checklist Execution")

        if len(schedules) == 0:
            st.info("No preventive schedules configured.")
        else:
            sched_df = pd.DataFrame(schedules)
            st.dataframe(
                sched_df[["Schedule ID", "Product ID", "Task Title", "Frequency", "Technician", "Next Due Date", "Status"]], 
                use_container_width=True
            )

            st.markdown("### 🛠️ Perform Task / Complete Checklist")
            
            selected_sched_id = st.selectbox(
                "Select Schedule to Execute",
                options=[s["Schedule ID"] for s in schedules],
                format_func=lambda x: f"{x} - {next(item['Task Title'] for item in schedules if item['Schedule ID'] == x)} ({next(item['Product ID'] for item in schedules if item['Schedule ID'] == x)})"
            )

            selected_task = next(s for s in schedules if s["Schedule ID"] == selected_sched_id)

            col_details, col_check = st.columns([1, 1])

            with col_details:
                st.info(f"""
                **Schedule ID:** `{selected_task['Schedule ID']}`  
                **Machine:** `{selected_task['Product ID']}`  
                **Frequency:** `{selected_task['Frequency']}`  
                **Technician:** `{selected_task['Technician']}`  
                **Next Due Date:** `{selected_task['Next Due Date']}`  
                **Status:** `{selected_task['Status']}`
                """)

                if st.button("⚡ Generate Work Order from Task"):
                    wo_count = len(st.session_state["work_orders"])
                    new_wo = {
                        "Work Order ID": f"WO-2026-{wo_count + 1:03d}",
                        "Product ID": selected_task["Product ID"],
                        "Issue": f"Preventive Maintenance: {selected_task['Task Title']}",
                        "Priority": "High" if selected_task["Status"] == "Overdue" else "Medium",
                        "Technician": selected_task["Technician"],
                        "Due Date": selected_task["Next Due Date"],
                        "Status": "Assigned"
                    }
                    st.session_state["work_orders"].append(new_wo)
                    st.success(f"✅ Work Order `{new_wo['Work Order ID']}` created and sent to Module 4 Hub!")

            with col_check:
                st.markdown("#### 📝 Maintenance Checklist")
                completed_checks = []
                for item in selected_task["Checklist"]:
                    checked = st.checkbox(item, key=f"chk_{selected_sched_id}_{item}")
                    if checked:
                        completed_checks.append(item)

                notes = st.text_area("Technician Notes", placeholder="e.g., Checked oil pressure, cleaned filters.")

                if st.button("✅ Complete Maintenance Task"):
                    if len(completed_checks) < len(selected_task["Checklist"]):
                        st.warning("⚠️ Complete all checklist items before submitting!")
                    else:
                        # Add to history
                        history_entry = {
                            "Schedule ID": selected_task["Schedule ID"],
                            "Product ID": selected_task["Product ID"],
                            "Task Title": selected_task["Task Title"],
                            "Technician": selected_task["Technician"],
                            "Completion Date": str(date.today()),
                            "Notes": notes
                        }
                        st.session_state["pm_history"].append(history_entry)

                        # Update next due date
                        current_due = datetime.strptime(selected_task["Next Due Date"], "%Y-%m-%d").date()
                        freq = selected_task["Frequency"]
                        
                        freq_days = {
                            "Daily": 1,
                            "Weekly": 7,
                            "Monthly": 30,
                            "Quarterly": 90,
                            "Annual": 365
                        }
                        next_due = current_due + timedelta(days=freq_days.get(freq, 7))

                        selected_task["Last Completed"] = str(date.today())
                        selected_task["Next Due Date"] = str(next_due)
                        selected_task["Status"] = "Scheduled"

                        st.balloons()
                        st.success(f"🎉 Task completed! Next due date updated to `{next_due}`.")
                        st.rerun()

    # ------------------------------------
    # TAB 2: CONFIGURE SCHEDULE
    # ------------------------------------
    with tab_create:
        st.subheader("➕ Create New Schedule")
        all_ids = sorted(df["Product ID"].astype(str).unique())

        with st.form("create_pm_form", clear_on_submit=True):
            f_prod_id = st.selectbox("Target Product ID", options=all_ids)
            f_task_title = st.text_input("Task Title", placeholder="e.g., Hydraulic Pressure Check & Filter Replacement")
            
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                f_freq = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly", "Quarterly", "Annual"])
                f_tech = st.selectbox("Technician", ["Rahul", "Anita", "John", "Priya"])
            with f_col2:
                f_start_date = st.date_input("First Execution Date", date.today() + timedelta(days=7))
                f_checklist_raw = st.text_area("Checklist Items (comma-separated)", value="Check fluid level, Inspect seals, Measure telemetry")

            pm_submit = st.form_submit_button("📅 Save Schedule")

        if pm_submit:
            checklist_items = [item.strip() for item in f_checklist_raw.split(",") if item.strip()]
            sched_num = len(st.session_state["pm_schedules"]) + 101
            
            new_pm = {
                "Schedule ID": f"PM-{sched_num}",
                "Product ID": f_prod_id,
                "Task Title": f_task_title,
                "Frequency": f_freq,
                "Technician": f_tech,
                "Next Due Date": str(f_start_date),
                "Status": "Scheduled",
                "Checklist": checklist_items,
                "Last Completed": "Never"
            }
            
            st.session_state["pm_schedules"].append(new_pm)
            st.success(f"✅ Created schedule `{new_pm['Schedule ID']}`!")
            st.rerun()

    # ------------------------------------
    # TAB 3: AI RECOMMENDATIONS
    # ------------------------------------
    with tab_ai:
        st.subheader("🤖 AI Preventive Plan Generator")
        ai_prod_id = st.selectbox("Select Machine for AI Plan", options=sorted(df["Product ID"].astype(str).unique()), key="ai_select")
        
        target_machine = df[df["Product ID"].astype(str) == ai_prod_id].iloc[0]

        m1, m2 = st.columns(2)
        m1.metric("Machine Type", target_machine["Type"])
        m2.metric("Tool Wear", f"{target_machine['Tool wear [min]']} min")

        if st.button("🤖 Generate Recommendations"):
            with st.spinner("Analyzing machine telemetry..."):
                plan = generate_pm_recommendations(
                    target_machine["Type"], 
                    target_machine["Tool wear [min]"], 
                    target_machine["Machine failure"]
                )
                st.session_state["ai_pm_plan"] = plan

        if "ai_pm_plan" in st.session_state:
            st.markdown("---")
            st.markdown(st.session_state["ai_pm_plan"])

    # ------------------------------------
    # TAB 4: HISTORY LOGS
    # ------------------------------------
    with tab_history:
        st.subheader("📜 Completed Maintenance History")
        history_list = st.session_state["pm_history"]

        if len(history_list) == 0:
            st.info("No logs found. Complete tasks in Tab 1 to record history.")
        else:
            st.dataframe(pd.DataFrame(history_list), use_container_width=True)
            if st.button("🗑️ Clear History Logs"):
                st.session_state["pm_history"] = []
                st.rerun()