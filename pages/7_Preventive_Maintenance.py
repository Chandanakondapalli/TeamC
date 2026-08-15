import streamlit as st
import pandas as pd

from datetime import datetime, timedelta

from preventive_database import (
    create_schedule,
    get_schedules,
    update_schedule,
    delete_schedule
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Preventive Maintenance",
    page_icon="🗓️",
    layout="wide"
)


# =========================================================
# LOGIN CHECK
# =========================================================

if not st.session_state.get("logged_in", False):

    st.warning("🔒 Please login first.")

    st.stop()


# =========================================================
# GET USER INFORMATION
# =========================================================

username = st.session_state.get(
    "username",
    ""
)

role = st.session_state.get(
    "role",
    ""
)


# =========================================================
# ROLE CHECK
# =========================================================

if role not in ["Admin", "Technician"]:

    st.error(
        "❌ You do not have permission to access this page."
    )

    st.stop()


# =========================================================
# TITLE
# =========================================================

st.title(
    "🗓️ Preventive Maintenance Scheduler"
)

if role == "Admin":

    st.write(
        "Create preventive maintenance schedules, "
        "assign technicians, monitor overdue tasks, "
        "and manage maintenance activities."
    )

else:

    st.write(
        f"View and manage preventive maintenance tasks "
        f"assigned to {username}."
    )


# =========================================================
# LOAD SCHEDULES
# =========================================================

rows, columns = get_schedules()

schedule_df = pd.DataFrame(
    rows,
    columns=columns
)


# =========================================================
# HANDLE EMPTY DATABASE
# =========================================================

if schedule_df.empty:

    st.info(
        "📭 No preventive maintenance schedules available."
    )

    # Admin can still create a schedule
    # so don't stop for Admin.

    if role != "Admin":

        st.stop()


# =========================================================
# ROLE-BASED FILTER
# =========================================================

if not schedule_df.empty:

    if role == "Technician":

        # Convert both values to lowercase
        # so Priya, priya, PRIYA all match.

        logged_technician = (
            username
            .strip()
            .lower()
        )

        schedule_df["technician_normalized"] = (
            schedule_df["technician"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        # Technician sees ONLY their schedules

        schedule_df = schedule_df[
            schedule_df["technician_normalized"]
            ==
            logged_technician
        ].copy()

        # Remove helper column

        schedule_df.drop(
            columns=["technician_normalized"],
            inplace=True
        )


# =========================================================
# TECHNICIAN - NO TASKS
# =========================================================

if role == "Technician" and schedule_df.empty:

    st.warning(
        f"📭 No preventive maintenance tasks "
        f"are currently assigned to {username}."
    )

    st.info(
        "When an administrator assigns a maintenance "
        "task to you, it will appear here."
    )

    st.stop()


# =========================================================
# MACHINE SELECTION
# =========================================================

machine = None

if "selected_machine" in st.session_state:

    machine = st.session_state[
        "selected_machine"
    ]


# =========================================================
# ADMIN - CREATE SCHEDULE
# =========================================================

if role == "Admin":

    st.markdown("---")

    st.subheader(
        "📝 Create Maintenance Schedule"
    )

    # -----------------------------------------------------
    # MACHINE CHECK
    # -----------------------------------------------------

    if machine is None:

        st.warning(
            "⚠️ Please select a machine from "
            "Machine Explorer before creating a schedule."
        )

    else:

        # -------------------------------------------------
        # MACHINE DETAILS
        # -------------------------------------------------

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Product ID",
                machine["Product ID"]
            )

        with c2:

            st.metric(
                "Machine ID",
                machine["UDI"]
            )

        with c3:

            st.metric(
                "Machine Type",
                machine["Type"]
            )

        with c4:

            st.metric(
                "Tool Wear",
                machine["Tool wear [min]"]
            )


        st.markdown("---")


        # -------------------------------------------------
        # TECHNICIAN
        # -------------------------------------------------

        technician = st.selectbox(
            "👨‍🔧 Assign Technician",
            [
                "Arun",
                "Kumar",
                "Priya",
                "Meena"
            ]
        )


        # -------------------------------------------------
        # FREQUENCY
        # -------------------------------------------------

        frequency = st.selectbox(
            "📅 Maintenance Frequency",
            [
                "Daily",
                "Weekly",
                "Monthly",
                "Quarterly",
                "Yearly"
            ]
        )


        # -------------------------------------------------
        # CALCULATE NEXT DATE
        # -------------------------------------------------

        today = datetime.now()


        if frequency == "Daily":

            next_date = (
                today
                +
                timedelta(days=1)
            )


        elif frequency == "Weekly":

            next_date = (
                today
                +
                timedelta(days=7)
            )


        elif frequency == "Monthly":

            next_date = (
                today
                +
                timedelta(days=30)
            )


        elif frequency == "Quarterly":

            next_date = (
                today
                +
                timedelta(days=90)
            )


        else:

            next_date = (
                today
                +
                timedelta(days=365)
            )


        st.info(
            "📅 Next Maintenance Date: "
            +
            next_date.strftime("%Y-%m-%d")
        )


        # -------------------------------------------------
        # TASK
        # -------------------------------------------------

        task = st.text_area(
            "🛠️ Maintenance Task",
            value=(
                "Perform preventive maintenance "
                "and inspect machine components."
            )
        )


        # -------------------------------------------------
        # CREATE SCHEDULE
        # -------------------------------------------------

        if st.button(
            "➕ Create Schedule",
            use_container_width=True
        ):

            schedule_id = (
                "PM-"
                +
                datetime.now().strftime(
                    "%Y%m%d%H%M%S"
                )
            )


            create_schedule(

                schedule_id=schedule_id,

                product_id=machine[
                    "Product ID"
                ],

                machine_id=int(
                    machine["UDI"]
                ),

                technician=technician,

                frequency=frequency,

                task=task,

                status="Scheduled",

                next_date=next_date.strftime(
                    "%Y-%m-%d"
                ),

                created_date=datetime.now().strftime(
                    "%Y-%m-%d"
                )
            )


            st.success(
                f"✅ Maintenance schedule created "
                f"and assigned to {technician}."
            )


            st.rerun()


# =========================================================
# DASHBOARD
# =========================================================

if not schedule_df.empty:

    st.markdown("---")

    if role == "Admin":

        st.subheader(
            "📊 Maintenance Dashboard"
        )

    else:

        st.subheader(
            f"📊 My Maintenance Dashboard - {username}"
        )


    # -----------------------------------------------------
    # COUNT STATUS
    # -----------------------------------------------------

    total = len(schedule_df)


    scheduled = len(
        schedule_df[
            schedule_df["status"]
            ==
            "Scheduled"
        ]
    )


    in_progress = len(
        schedule_df[
            schedule_df["status"]
            ==
            "In Progress"
        ]
    )


    completed = len(
        schedule_df[
            schedule_df["status"]
            ==
            "Completed"
        ]
    )


    overdue = len(
        schedule_df[
            schedule_df["status"]
            ==
            "Overdue"
        ]
    )


    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    c1, c2, c3, c4, c5 = st.columns(5)


    with c1:

        st.metric(
            "📋 Total",
            total
        )


    with c2:

        st.metric(
            "🗓 Scheduled",
            scheduled
        )


    with c3:

        st.metric(
            "🔄 In Progress",
            in_progress
        )


    with c4:

        st.metric(
            "✅ Completed",
            completed
        )


    with c5:

        st.metric(
            "⚠️ Overdue",
            overdue
        )


# =========================================================
# SEARCH
# =========================================================

if not schedule_df.empty:

    st.markdown("---")

    st.subheader(
        "🔍 Search Maintenance Tasks"
    )


    search_text = st.text_input(
        "Search by Schedule ID, Product ID, "
        "Technician, or Task"
    )


    filtered_df = schedule_df.copy()


    if search_text:

        filtered_df = filtered_df[
            filtered_df
            .astype(str)
            .apply(
                lambda row:
                row.str.contains(
                    search_text,
                    case=False,
                    na=False
                ).any(),
                axis=1
            )
        ]


# =========================================================
# ADMIN TECHNICIAN FILTER
# =========================================================

if (
    role == "Admin"
    and not schedule_df.empty
):

    st.subheader(
        "👨‍🔧 Filter by Technician"
    )


    technician_filter = st.selectbox(
        "Select Technician",
        [
            "All"
        ]
        +
        sorted(
            schedule_df[
                "technician"
            ]
            .astype(str)
            .unique()
            .tolist()
        )
    )


    if technician_filter != "All":

        filtered_df = filtered_df[
            filtered_df["technician"]
            ==
            technician_filter
        ]


# =========================================================
# DISPLAY MAINTENANCE TASKS
# =========================================================

if not schedule_df.empty:

    st.markdown("---")


    if role == "Admin":

        st.subheader(
            "📋 All Maintenance Schedules"
        )

    else:

        st.subheader(
            "📋 My Assigned Maintenance Tasks"
        )


    # Columns to display

    display_columns = [
        "schedule_id",
        "product_id",
        "machine_id",
        "technician",
        "frequency",
        "task",
        "status",
        "next_date",
        "created_date"
    ]


    available_columns = [
        column
        for column in display_columns
        if column in filtered_df.columns
    ]


    st.dataframe(
        filtered_df[
            available_columns
        ],
        width="stretch",
        hide_index=True
    )


# =========================================================
# OVERDUE MONITORING
# =========================================================

if not schedule_df.empty:

    st.markdown("---")

    st.subheader(
        "⚠️ Overdue Maintenance"
    )


    today_date = datetime.now().date()


    overdue_records = []


    for index, row in schedule_df.iterrows():

        try:

            schedule_date = datetime.strptime(
                str(row["next_date"]),
                "%Y-%m-%d"
            ).date()

        except:

            continue


        if (
            schedule_date < today_date
            and row["status"] != "Completed"
        ):

            overdue_records.append(
                row
            )


            # Update database

            update_schedule(
                row["schedule_id"],
                "Overdue"
            )


    # -----------------------------------------------------
    # SHOW OVERDUE
    # -----------------------------------------------------

    if overdue_records:

        overdue_df = pd.DataFrame(
            overdue_records
        )


        st.error(
            f"⚠️ {len(overdue_df)} "
            "overdue maintenance task(s) found."
        )


        st.dataframe(
            overdue_df[
                [
                    "schedule_id",
                    "product_id",
                    "technician",
                    "task",
                    "next_date",
                    "status"
                ]
            ],
            width="stretch",
            hide_index=True
        )


    else:

        st.success(
            "✅ No overdue maintenance tasks."
        )


# =========================================================
# MAINTENANCE CALENDAR
# =========================================================

if not schedule_df.empty:

    st.markdown("---")

    st.subheader(
        "📅 Maintenance Calendar"
    )


    calendar_columns = [
        "schedule_id",
        "product_id",
        "technician",
        "task",
        "next_date",
        "status"
    ]


    available_calendar_columns = [
        column
        for column in calendar_columns
        if column in schedule_df.columns
    ]


    st.dataframe(
        schedule_df[
            available_calendar_columns
        ],
        width="stretch",
        hide_index=True
    )


# =========================================================
# UPDATE STATUS
# =========================================================

if not schedule_df.empty:

    st.markdown("---")

    st.subheader(
        "🔄 Update Maintenance Status"
    )


    schedule_ids = (
        schedule_df[
            "schedule_id"
        ]
        .astype(str)
        .tolist()
    )


    selected_schedule = st.selectbox(
        "Select Schedule",
        schedule_ids,
        key="update_schedule"
    )


    status_options = [
        "Scheduled",
        "In Progress",
        "Completed",
        "Overdue"
    ]


    new_status = st.selectbox(
        "Select New Status",
        status_options,
        key="new_status"
    )


    if st.button(
        "🔄 Update Status",
        use_container_width=True
    ):

        update_schedule(
            selected_schedule,
            new_status
        )


        st.success(
            "✅ Maintenance status updated successfully."
        )


        st.rerun()


# =========================================================
# DELETE SCHEDULE - ADMIN ONLY
# =========================================================

if (
    role == "Admin"
    and not schedule_df.empty
):

    st.markdown("---")

    st.subheader(
        "🗑️ Delete Maintenance Schedule"
    )


    delete_schedule_id = st.selectbox(
        "Select Schedule ID",
        schedule_df[
            "schedule_id"
        ]
        .astype(str)
        .tolist(),
        key="delete_schedule"
    )


    if st.button(
        "🗑️ Delete Schedule",
        use_container_width=True
    ):

        delete_schedule(
            delete_schedule_id
        )


        st.success(
            "🗑️ Maintenance schedule deleted."
        )


        st.rerun()


# =========================================================
# TECHNICIAN INFORMATION
# =========================================================

if role == "Technician":

    st.markdown("---")


    st.info(
        f"👨‍🔧 Logged in as Technician: {username}"
    )


    st.caption(
        "You can only view and update maintenance "
        "tasks assigned to you."
    )


# =========================================================
# ADMIN INFORMATION
# =========================================================

if role == "Admin":

    st.markdown("---")


    st.info(
        "👑 Logged in as Administrator"
    )


    st.caption(
        "Administrator can view and manage "
        "all preventive maintenance schedules."
    )