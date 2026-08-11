import streamlit as st
import pandas as pd
import os
from datetime import date
from utils.pdf_generator import generate_workorder_pdf
from utils.ui import page_header, load_css
from utils.themes import *
from utils.database import *
from utils.ai_report import *
from utils.auth import require_login, hide_login_from_sidebar

require_login()
hide_login_from_sidebar()

# --------------------------------------------------
# Database & Config
# --------------------------------------------------
init_db()
create_users_table()
seed_users()

st.set_page_config(
    page_title="Work Orders | Agentic FacilityOps",
    page_icon="📝",
    layout="wide"
)
load_css()

# ============================================================
# CURRENT USER
# ============================================================

user_role = st.session_state.get("user_role")
user_name = st.session_state.get("user_name")


# ============================================================
# LOAD & FILTER WORK ORDERS
# ============================================================

workorder_df = get_all_work_orders()

if user_role == "Technician":

    workorder_df = workorder_df[
        workorder_df["technician"].astype(str).str.strip()
        == str(user_name).strip()
    ].copy()

elif user_role == "Employee":

    workorder_df = workorder_df.copy()

else:

    workorder_df = workorder_df.iloc[0:0]


# ============================================================
# USER MESSAGE
# ============================================================

if user_role == "Technician":

    st.info(
        f"👨‍🔧 Showing work orders assigned to **{user_name}**"
    )

elif user_role == "Employee":

    st.info(
        "👤 Showing all work orders"
    )

page_header(
    "📝",
    "Work Orders",
    "Create, manage and monitor maintenance work orders."
)
defaults = {
    "page_mode": "home",
    "selected_order": None,
    "created_order": None,
    "edit_workorder": False,
    "status_updated": False,
    "workorder_deleted": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ADD this data loading block
@st.cache_data
def load_machine_data():
    file_path = "data/ai4i2020.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame()

# Create the machine_df variable
machine_df = load_machine_data()
# --------------------------------------------------
# KPI Cards
# --------------------------------------------------
kpis = get_kpis()
st.markdown("## 📊 Work Order Overview")
c1, c2, c3, c4 = st.columns(4)
c1.metric("📋 Total Orders", kpis["Total"])
c2.metric("🟡 Open", kpis["Open"])
c3.metric("🟢 Completed", kpis["Completed"])
c4.metric("🔴 High Priority", kpis["High"])

st.divider()

# --------------------------------------------------
# Maintenance Action Center
# --------------------------------------------------
with st.container(border=True):
    st.markdown("## 🚀 Maintenance Action Center")
    st.caption("Create, assign and monitor maintenance work orders for facility assets.")

    create_tab, details_tab = st.tabs([
        "➕ Create Work Order",
        "📄 Work Order Details"
    ])

    # --- TAB 1: CREATE WORK ORDER ---
    with create_tab:
        if st.session_state.page_mode == "home":
            st.info("Create a maintenance work order to assign technicians and track activities.")
            if st.button("➕ Create New Work Order", type="primary", use_container_width=True):
                st.session_state.page_mode = "create"
                st.rerun()

        elif st.session_state.page_mode == "create":
            with st.form("create_workorder"):
                left, right = st.columns(2)
                with left:
                    st.markdown("#### 🔧 Machine Information")
                    machine_id = st.text_input("Machine ID")
                    machine_type = st.selectbox(
                        "Machine Type",
                        ["L", "M", "H"],
                        index=None,
                        placeholder="Select Machine Type"
                    )
                    maintenance_type = st.selectbox(
                        "Maintenance Type",
                        ["Preventive", "Predictive", "Corrective"],
                        index=None,
                        placeholder="Select Maintenance Type"
                    )
                    priority = st.selectbox(
                        "Priority",
                        ["Low", "Medium", "High"],
                        index=None,
                        placeholder="Select Priority"
                    )

                    auto_desc = ""
                    if machine_id:
                        # Check if the ID exists in our CSV
                        match = machine_df[machine_df["Product ID"] == machine_id]
                        if not match.empty:
                            # Generate the technical summary on the fly
                            auto_desc = get_technical_summary(match.iloc[0])

                with right:
                    st.markdown("#### 👨‍🔧 Assignment Details")
                    technician = st.selectbox(
                        "Assign Staff", 
                        options=["", "John Smith", "Sarah Wilson", "Michael Brown", "David Lee"],
                        format_func=lambda x: "Assign Personnel..." if x == "" else x
                    )
                    due_date = st.date_input("Due Date", min_value=date.today())
                    estimated_cost = st.number_input("Estimated Cost", value=2500.0, step=100.0)
                    estimated_time = st.text_input("Estimated Time", value="2 Hours")

                st.markdown("#### 📝 Work Description")
                description = st.text_area(
                    "Description", 
                    value=auto_desc, # This will be the AI text if available
                    height=150,
                    placeholder="AI details will appear here if machine was recently analyzed..."
                )
                
                col1, col2 = st.columns(2)
                if col1.form_submit_button("✅ Create Work Order", type="primary", use_container_width=True):
                    new_id = insert_work_order(
                        machine_id, machine_type, priority, maintenance_type,
                        technician, str(due_date), estimated_cost, estimated_time, description
                    )
                    st.session_state.created_order = new_id
                    st.session_state.page_mode = "created"
                    st.rerun()
                if col2.form_submit_button("❌ Cancel", type="primary", use_container_width=True):
                    st.session_state.page_mode = "home"
                    st.rerun()

        elif st.session_state.page_mode == "created":
            st.success(f"✅ Work Order **{st.session_state.created_order}** Created Successfully!")
            
            # Fetch the newly created order for the PDF
            work_order = get_work_order(st.session_state.created_order)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⬅ Back to Home", use_container_width=True):
                    st.session_state.page_mode = "home"
                    st.rerun()
            with col2:
                if work_order:
                    filename = f"WO_{work_order['work_order_id']}.pdf"
                    generate_workorder_pdf(work_order, filename)
                    with open(filename, "rb") as pdf:
                        st.download_button("📄 Download PDF", pdf, file_name=filename, mime="application/pdf", use_container_width=True, type="primary")

    # --- TAB 2: WORK ORDER DETAILS ---
    with details_tab:
        df_all = workorder_df.copy()
        selected_id = st.selectbox(
            "Select Work Order to View/Edit",
            options=df_all["work_order_id"].tolist(),
            index=None,
            placeholder="Select a Work Order"
        )

        if selected_id:
            work_order = get_work_order(selected_id)
            if work_order:
                if not st.session_state.edit_workorder:
                    # VIEW MODE
                    if not st.session_state.edit_workorder:

    # ========================================================
    # VIEW MODE - TEXT / CARD DISPLAY
    # ========================================================

                        st.markdown(f"### 📄 Work Order {selected_id}")

                        # Basic information
                        with st.container(border=True):

                            st.markdown("#### 🔧 Work Order Information")

                            c1, c2, c3 = st.columns(3)

                            with c1:
                                st.markdown("**Work Order ID**")
                                st.write(work_order["work_order_id"])

                            with c2:
                                st.markdown("**Machine ID**")
                                st.write(work_order["machine_id"])

                            with c3:
                                st.markdown("**Machine Type**")
                                st.write(work_order["machine_type"])


                        # Maintenance information
                        with st.container(border=True):

                            st.markdown("#### 🛠 Maintenance Details")

                            c1, c2, c3 = st.columns(3)

                            with c1:
                                st.markdown("**Maintenance Type**")
                                st.write(work_order["maintenance_type"])

                            with c2:
                                st.markdown("**Priority**")
                                st.write(work_order["priority"])

                            with c3:
                                st.markdown("**Status**")
                                st.write(work_order["status"])


                        # Assignment information
                        with st.container(border=True):

                            st.markdown("#### 👨‍🔧 Assignment & Schedule")

                            c1, c2, c3 = st.columns(3)

                            with c1:
                                st.markdown("**Technician**")
                                st.write(work_order["technician"])

                            with c2:
                                st.markdown("**Due Date**")
                                st.write(work_order["due_date"])

                            with c3:
                                st.markdown("**Estimated Time**")
                                st.write(work_order["estimated_time"])


            # Cost
                        with st.container(border=True):

                            st.markdown("#### 💰 Estimated Cost")

                            st.markdown(
                                f"### ₹ {work_order['estimated_cost']}"
                            )


                        # Description
                        with st.container(border=True):

                            st.markdown("#### 📝 Work Order Description")

                            st.markdown(
                                work_order["description"]
                                if work_order["description"]
                                else "No description provided."
                        )


                        st.divider()

                        # Actions
                        btn1, btn2 = st.columns(2)

                        with btn1:

                            fname = f"WO_{selected_id}.pdf"

                            generate_workorder_pdf(
                                work_order,
                                fname
                            )

                            with open(fname, "rb") as f:

                                st.download_button(
                                    "📄 Download Work Order PDF",
                                    f,
                                    file_name=fname,
                                    use_container_width=True,
                                    type="primary"
                                )


                        with btn2:

                            if st.button(
                                "✏️ Edit Work Order",
                                use_container_width=True
                            ):

                                st.session_state.edit_workorder = True

                                st.rerun()
                else:
                    # EDIT MODE
                    with st.form("edit_form"):
                        st.markdown(f"### Editing Work Order: {selected_id}")
                        c1, c2 = st.columns(2)
                        with c1:
                            u_tech = st.text_input("Technician", work_order["technician"])
                            u_priority = st.selectbox("Priority", ["Low", "Medium", "High"], 
                                                     index=["Low", "Medium", "High"].index(work_order["priority"]))
                            u_status = st.selectbox("Status", ["Open", "In Progress", "Completed"], 
                                                   index=["Open", "In Progress", "Completed"].index(work_order["status"]))
                        with c2:
                            u_due = st.date_input("Due Date", pd.to_datetime(work_order["due_date"]))
                            
                            # --- FIXED COST LOGIC ---
                            # Clean comma from string '2,500' -> '2500'
                            clean_cost = str(work_order["estimated_cost"]).replace(',', '')
                            u_cost = st.number_input("Cost ($)", value=float(clean_cost), step=10.0)
                            
                            u_time = st.text_input("Time Estimation", work_order["estimated_time"])
                        
                        u_desc = st.text_area("Description", work_order["description"])
                        
                        # Form Buttons
                        sc1, sc2 = st.columns(2)
                        if sc1.form_submit_button("💾 Save Changes", type="primary", use_container_width=True):
                            update_work_order(
                                selected_id, 
                                work_order["machine_id"], 
                                work_order["machine_type"], 
                                u_priority, 
                                work_order["maintenance_type"], 
                                u_tech, 
                                u_status, 
                                u_due.strftime("%Y-%m-%d"), 
                                u_cost, 
                                u_time, 
                                u_desc
                            )
                            st.session_state.edit_workorder = False
                            st.rerun()
                            
                        if sc2.form_submit_button("Cancel",type="primary", use_container_width=True):
                            st.session_state.edit_workorder = False
                            st.rerun()

# --------------------------------------------------
# Search & Manage Table
# --------------------------------------------------
with st.container(border=True):
    st.markdown("## 📋 Work Order Registry")
    
    # Filters
    f1, f2, f3 = st.columns(3)
    search_q = f1.text_input("🔍 Search ID or Machine")
    prio_f = f2.selectbox("Filter Priority", ["All", "High", "Medium", "Low"])
    stat_f = f3.selectbox("Filter Status", ["All", "Open", "In Progress", "Completed"])

    df = workorder_df.copy()
    if search_q:
        df = df[df["work_order_id"].str.contains(search_q, case=False) | df["machine_id"].str.contains(search_q, case=False)]
    if prio_f != "All":
        df = df[df["priority"] == prio_f]
    if stat_f != "All":
        df = df[df["status"] == stat_f]

    st.dataframe(df, use_container_width=True, hide_index=True, height=250)

    # Management Actions
    st.divider()
    st.markdown("### 🔧 Quick Actions")
    tab_upd, tab_del = st.tabs(["🔄 Update Status", "🗑 Delete Order"])

    with tab_upd:
        if st.session_state.status_updated:
            st.toast("Status updated!", icon="✅")
            st.session_state.status_updated = False

        sel_upd = st.selectbox(
            "Select Order to Update",
            options=df["work_order_id"].tolist(),
            index=None,
            placeholder="Select a Work Order",
            key="upd_sel"
        )
        if sel_upd:
            current_s = df[df["work_order_id"] == sel_upd]["status"].values[0]
            new_s = st.selectbox(
                "New Status",
                ["Open", "In Progress", "Completed"],
                index=None,
                placeholder="Select New Status"
            )
            if st.button("Update Status", type="primary", use_container_width=True):
                update_work_order_status(sel_upd, new_s)
                st.session_state.status_updated = True
                st.rerun()

    with tab_del:
        if st.session_state.workorder_deleted:
            st.toast("Work order deleted.", icon="🗑️")
            st.session_state.workorder_deleted = False

        sel_del = st.selectbox(
            "Select Order to Delete",
            options=df["work_order_id"].tolist(),
            index=None,
            placeholder="Select a Work Order",
            key="del_sel"
        )
        if sel_del:
            st.warning("⚠️ This action is permanent.")
            if st.button("Confirm Deletion", use_container_width=True):
                delete_work_order(sel_del)
                st.session_state.workorder_deleted = True
                st.rerun()