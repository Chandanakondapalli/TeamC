import streamlit as st
import pandas as pd


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Machine Explorer",
    page_icon="🏭",
    layout="wide"
)


# =========================================================
# LOGIN CHECK
# =========================================================

if not st.session_state.get("logged_in", False):

    st.warning("🔒 Please login first.")

    st.stop()


# =========================================================
# GET USER ROLE
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
# ROLE ACCESS
# =========================================================

# Admin and Technician are allowed

if role not in ["Admin", "Technician"]:

    st.error(
        "❌ Access denied."
    )

    st.stop()


# =========================================================
# TITLE
# =========================================================

st.title(
    "🏭 Machine Explorer"
)

st.write(
    "Search and analyze individual machine information, "
    "sensor values, failure conditions, and maintenance status."
)


st.markdown("---")


# =========================================================
# LOAD DATASET
# =========================================================

@st.cache_data
def load_data():

    try:

        df = pd.read_csv(
            "dataset/ai4i2020.csv"
        )

        return df

    except FileNotFoundError:

        st.error(
            "❌ ai4i2020.csv file not found."
        )

        return pd.DataFrame()


df = load_data()


if df.empty:

    st.stop()


# =========================================================
# MACHINE SEARCH
# =========================================================

st.subheader(
    "🔍 Search Machine"
)


search_type = st.radio(
    "Search using:",
    [
        "Product ID",
        "Machine ID (UDI)"
    ],
    horizontal=True
)


# =========================================================
# PRODUCT ID SEARCH
# =========================================================

if search_type == "Product ID":

    product_ids = sorted(
        df["Product ID"]
        .astype(str)
        .unique()
        .tolist()
    )


    selected_product = st.selectbox(
        "Select Product ID",
        ["Select a machine"] + product_ids
    )


    if selected_product == "Select a machine":

        st.info(
            "👆 Please select a Product ID."
        )

        st.stop()


    selected_machine_df = df[
        df["Product ID"].astype(str)
        ==
        selected_product
    ]


# =========================================================
# UDI SEARCH
# =========================================================

else:

    udi_values = sorted(
        df["UDI"]
        .unique()
        .tolist()
    )


    selected_udi = st.selectbox(
        "Select Machine ID (UDI)",
        ["Select a machine"] + udi_values
    )


    if selected_udi == "Select a machine":

        st.info(
            "👆 Please select a Machine ID."
        )

        st.stop()


    selected_machine_df = df[
        df["UDI"]
        ==
        selected_udi
    ]


# =========================================================
# GET MACHINE
# =========================================================

if selected_machine_df.empty:

    st.error(
        "Machine not found."
    )

    st.stop()


machine = selected_machine_df.iloc[0]


# =========================================================
# STORE SELECTED MACHINE
# =========================================================

st.session_state[
    "selected_machine"
] = machine.to_dict()


# =========================================================
# MACHINE HEADER
# =========================================================

st.markdown("---")

st.subheader(
    "🏭 Machine Information"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Product ID",
        machine["Product ID"]
    )


with col2:

    st.metric(
        "Machine ID",
        machine["UDI"]
    )


with col3:

    st.metric(
        "Machine Type",
        machine["Type"]
    )


with col4:

    machine_failure = int(
        machine["Machine failure"]
    )


    if machine_failure == 1:

        st.metric(
            "Machine Status",
            "⚠️ Failed"
        )

    else:

        st.metric(
            "Machine Status",
            "✅ Normal"
        )


# =========================================================
# SENSOR VALUES
# =========================================================

st.markdown("---")

st.subheader(
    "📡 Live Sensor Values"
)


col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "Air Temperature",
        f"{machine['Air temperature [K]']:.2f} K"
    )


with col2:

    st.metric(
        "Process Temperature",
        f"{machine['Process temperature [K]']:.2f} K"
    )


with col3:

    st.metric(
        "Rotational Speed",
        f"{machine['Rotational speed [rpm]']:.0f} RPM"
    )


with col4:

    st.metric(
        "Torque",
        f"{machine['Torque [Nm]']:.2f} Nm"
    )


with col5:

    st.metric(
        "Tool Wear",
        f"{machine['Tool wear [min]']:.0f} min"
    )


# =========================================================
# MACHINE HEALTH
# =========================================================

st.markdown("---")

st.subheader(
    "❤️ Machine Health"
)


tool_wear = float(
    machine["Tool wear [min]"]
)


if tool_wear < 100:

    health = "Excellent"

    health_message = (
        "Machine is operating normally."
    )


elif tool_wear < 180:

    health = "Monitor"

    health_message = (
        "Machine requires monitoring."
    )


else:

    health = "Maintenance Required"

    health_message = (
        "Preventive maintenance is recommended."
    )


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Machine Health",
        health
    )


with col2:

    st.write(
        health_message
    )


st.progress(
    min(
        tool_wear / 200,
        1.0
    )
)


st.caption(
    f"Tool Wear: {tool_wear:.0f} / 200 minutes"
)


# =========================================================
# FAILURE ANALYSIS
# =========================================================

st.markdown("---")

st.subheader(
    "⚠️ Failure Analysis"
)


failure_data = {

    "Machine Failure":
        int(machine["Machine failure"]),

    "Tool Wear Failure (TWF)":
        int(machine["TWF"]),

    "Heat Dissipation Failure (HDF)":
        int(machine["HDF"]),

    "Power Failure (PWF)":
        int(machine["PWF"]),

    "Overstrain Failure (OSF)":
        int(machine["OSF"]),

    "Random Failure (RNF)":
        int(machine["RNF"])
}


failure_df = pd.DataFrame(
    {
        "Failure Type":
            list(failure_data.keys()),

        "Status":
            [
                "Failure"
                if value == 1
                else "Normal"

                for value in failure_data.values()
            ]
    }
)


st.dataframe(
    failure_df,
    width="stretch",
    hide_index=True
)


# =========================================================
# FAILURE WARNING
# =========================================================

failure_columns = [
    "TWF",
    "HDF",
    "PWF",
    "OSF",
    "RNF"
]


active_failures = []


for column in failure_columns:

    if int(machine[column]) == 1:

        active_failures.append(
            column
        )


if active_failures:

    st.error(
        "⚠️ Failure detected: "
        +
        ", ".join(active_failures)
    )

else:

    st.success(
        "✅ No specific failure mode detected."
    )


# =========================================================
# MACHINE DETAILS
# =========================================================

st.markdown("---")

st.subheader(
    "📋 Complete Machine Details"
)


details = pd.DataFrame(
    {
        "Parameter": [

            "Product ID",
            "Machine ID",
            "Machine Type",
            "Air Temperature",
            "Process Temperature",
            "Rotational Speed",
            "Torque",
            "Tool Wear",
            "Machine Failure",
            "TWF",
            "HDF",
            "PWF",
            "OSF",
            "RNF"
        ],

        "Value": [

            machine["Product ID"],
            machine["UDI"],
            machine["Type"],
            f"{machine['Air temperature [K]']} K",
            f"{machine['Process temperature [K]']} K",
            f"{machine['Rotational speed [rpm]']} RPM",
            f"{machine['Torque [Nm]']} Nm",
            f"{machine['Tool wear [min]']} min",
            machine["Machine failure"],
            machine["TWF"],
            machine["HDF"],
            machine["PWF"],
            machine["OSF"],
            machine["RNF"]
        ]
    }
)


st.dataframe(
    details,
    width="stretch",
    hide_index=True
)


# =========================================================
# MAINTENANCE RECOMMENDATION
# =========================================================

st.markdown("---")

st.subheader(
    "🛠️ Maintenance Recommendation"
)


if active_failures:

    st.warning(
        "⚠️ This machine requires maintenance attention."
    )


    if "TWF" in active_failures:

        st.write(
            "🔧 Inspect and replace worn tools."
        )


    if "HDF" in active_failures:

        st.write(
            "🌡️ Check cooling and heat dissipation systems."
        )


    if "PWF" in active_failures:

        st.write(
            "⚡ Inspect power supply and electrical components."
        )


    if "OSF" in active_failures:

        st.write(
            "🔩 Inspect machine load and mechanical components."
        )


    if "RNF" in active_failures:

        st.write(
            "🔍 Perform detailed machine inspection."
        )


elif tool_wear >= 180:

    st.warning(
        "⚠️ Tool wear is high. "
        "Preventive maintenance is recommended."
    )


else:

    st.success(
        "✅ No immediate maintenance required."
    )


# =========================================================
# USER INFORMATION
# =========================================================

st.markdown("---")

st.caption(
    f"Logged in as: {username} | Role: {role}"
)