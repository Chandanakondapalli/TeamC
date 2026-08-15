import streamlit as st
import pandas as pd

from work_order_database import (
    get_work_orders,
    get_technician_work_orders,
    update_work_order,
    delete_work_order
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Work Order Management",
    page_icon="📋",
    layout="wide"
)


# =========================================================
# LOGIN CHECK
# =========================================================

if not st.session_state.get("logged_in", False):

    st.warning("🔒 Please login first.")

    st.stop()


# =========================================================
# GET LOGIN INFORMATION
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
# TITLE
# =========================================================

st.title("📋 Work Order Management")

st.write(
    "View, search, filter, update, and manage maintenance work orders."
)


# =========================================================
# ROLE BASED WORK ORDER LOADING
# =========================================================

if role == "Admin":

    # Admin can see ALL work orders

    st.success(
        "👑 Logged in as Administrator"
    )

    rows, columns = get_work_orders()


elif role == "Technician":

    # Technician can see ONLY their own work orders

    st.info(
        f"👨‍🔧 Logged in as Technician: {username}"
    )

    rows, columns = get_technician_work_orders(
        username
    )


else:

    st.error(
        "❌ Invalid role."
    )

    st.stop()


# =========================================================
# CREATE DATAFRAME
# =========================================================

work_order_df = pd.DataFrame(
    rows,
    columns=columns
)


# =========================================================
# NO WORK ORDERS
# =========================================================

if work_order_df.empty:

    if role == "Admin":

        st.warning(
            "📭 No work orders have been created yet."
        )

        st.info(
            "Go to Work Order Creation and create a work order."
        )

    else:

        st.warning(
            f"📭 No work orders are currently assigned "
            f"to {username}."
        )

    st.stop()


# =========================================================
# ADMIN / TECHNICIAN SUMMARY
# =========================================================

if role == "Admin":

    st.success(
        f"✅ {len(work_order_df)} "
        f"work order(s) available in the system."
    )

else:

    st.success(
        f"✅ {len(work_order_df)} "
        f"work order(s) assigned to you."
    )


# =========================================================
# KPI CARDS
# =========================================================

st.markdown("---")

st.subheader(
    "📊 Work Order Dashboard"
)


total = len(work_order_df)


assigned = len(
    work_order_df[
        work_order_df["status"] == "Assigned"
    ]
)


in_progress = len(
    work_order_df[
        work_order_df["status"] == "In Progress"
    ]
)


completed = len(
    work_order_df[
        work_order_df["status"] == "Completed"
    ]
)


high_priority = len(
    work_order_df[
        work_order_df["priority"]
        .astype(str)
        .str.lower()
        .isin(
            [
                "high",
                "critical"
            ]
        )
    ]
)


c1, c2, c3, c4, c5 = st.columns(5)


c1.metric(
    "📋 Total",
    total
)

c2.metric(
    "📌 Assigned",
    assigned
)

c3.metric(
    "🔄 In Progress",
    in_progress
)

c4.metric(
    "✅ Completed",
    completed
)

c5.metric(
    "⚠ High Priority",
    high_priority
)


# =========================================================
# SEARCH
# =========================================================

st.markdown("---")

st.subheader(
    "🔍 Search Work Orders"
)


search_text = st.text_input(
    "Search by Work Order ID, Product ID, Machine, Technician or Task"
)


filtered_df = work_order_df.copy()


if search_text:

    search_text = (
        search_text
        .strip()
        .lower()
    )

    filtered_df = filtered_df[
        filtered_df.astype(str)
        .apply(
            lambda row:
            row.str.lower()
            .str.contains(
                search_text,
                na=False
            )
            .any(),
            axis=1
        )
    ]


# =========================================================
# STATUS FILTER
# =========================================================

status_options = [
    "All"
] + sorted(
    work_order_df["status"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


status_filter = st.selectbox(
    "📌 Filter by Status",
    status_options
)


if status_filter != "All":

    filtered_df = filtered_df[
        filtered_df["status"]
        ==
        status_filter
    ]


# =========================================================
# PRIORITY FILTER
# =========================================================

priority_options = [
    "All"
] + sorted(
    work_order_df["priority"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


priority_filter = st.selectbox(
    "⚠ Filter by Priority",
    priority_options
)


if priority_filter != "All":

    filtered_df = filtered_df[
        filtered_df["priority"]
        ==
        priority_filter
    ]


# =========================================================
# DISPLAY WORK ORDERS
# =========================================================

st.markdown("---")

st.subheader(
    "📋 Work Orders"
)


if filtered_df.empty:

    st.warning(
        "No work orders match your search/filter."
    )

else:

    st.dataframe(
        filtered_df,
        width="stretch",
        hide_index=True
    )


# =========================================================
# UPDATE STATUS
# =========================================================

st.markdown("---")

st.subheader(
    "🔄 Update Work Order Status"
)


work_order_ids = (
    work_order_df["work_order_id"]
    .tolist()
)


selected_work_order = st.selectbox(
    "Select Work Order",
    work_order_ids
)


new_status = st.selectbox(
    "Select New Status",
    [
        "Assigned",
        "In Progress",
        "Completed",
        "Cancelled"
    ]
)


if st.button(
    "🔄 Update Status",
    use_container_width=True
):

    update_work_order(
        selected_work_order,
        new_status
    )

    st.success(
        "✅ Work order status updated successfully."
    )

    st.rerun()


# =========================================================
# DELETE WORK ORDER
# =========================================================

if role == "Admin":

    st.markdown("---")

    st.subheader(
        "🗑 Delete Work Order"
    )

    delete_work_order_id = st.selectbox(
        "Select Work Order to Delete",
        work_order_ids,
        key="delete_work_order"
    )

    if st.button(
        "🗑 Delete Work Order",
        use_container_width=True
    ):

        delete_work_order(
            delete_work_order_id
        )

        st.success(
            "🗑 Work order deleted successfully."
        )

        st.rerun()