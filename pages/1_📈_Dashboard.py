# ---------------------------------
# Imports
# ---------------------------------

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils.ui import *
from utils.cards import *
from utils.charts import *
from utils.themes import *
load_css()
from utils.auth import require_login, hide_login_from_sidebar

require_login()
hide_login_from_sidebar()


sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 120
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 12

# ---------------------------------
# Page Configuration
# ---------------------------------

st.set_page_config(
    page_title="Agentic FacilityOps AI",
    page_icon="🏭",
    layout="wide"
)

# ---------------------------------
# Load Dataset
# ---------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/ai4i2020.csv")

df = load_data()

numeric_df = df.select_dtypes(include=np.number)

# ---------------------------------
# Dashboard Header
# ---------------------------------

page_header(
    "📈",
    "Predictive Maintenance Dashboard",
    "Monitor KPIs, failures and machine performance."
)

st.markdown("""
Welcome to the **Agentic FacilityOps AI Dashboard**.

This dashboard provides interactive analytics for monitoring machine performance,
analyzing equipment health, identifying failure patterns, and supporting predictive maintenance decisions.
""")

st.divider()

# ---------------------------------
# Dashboard Overview
# ---------------------------------

st.subheader("📊 Dashboard Overview")

st.caption(
    "Key performance indicators summarizing the predictive maintenance dataset."
)

# ---------------------------------
# Dashboard Metrics
# ---------------------------------

total_records = len(df)
total_features = len(df.columns)
machine_failures = df["Machine failure"].sum()
failure_rate = (machine_failures / total_records) * 100

average_rpm = df["Rotational speed [rpm]"].mean()
average_torque = df["Torque [Nm]"].mean()
average_toolwear = df["Tool wear [min]"].mean()
most_common_type = df["Type"].mode()[0]

failure_columns = ["TWF", "HDF", "PWF", "OSF", "RNF"]
most_common_failure = df[failure_columns].sum().idxmax()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📄 Total Records",
        f"{total_records:,}"
    )

with col2:
    st.metric(
        "📌 Total Features",
        total_features
    )

with col3:
    st.metric(
        "⚠ Machine Failures",
        machine_failures
    )

with col4:
    st.metric(
        "📉 Failure Rate",
        f"{failure_rate:.2f}%"
    )

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "⚙ Avg RPM",
        f"{average_rpm:.0f}"
    )

with col6:
    st.metric(
        "🔧 Avg Torque",
        f"{average_torque:.1f} Nm"
    )

with col7:
    st.metric(
        "🛠 Avg Tool Wear",
        f"{average_toolwear:.1f} min"
    )

with col8:
    st.metric(
        "⚠ Top Failure",
        most_common_failure
    )

st.divider()

# ---------------------------------
# Interactive Filters
# ---------------------------------

st.subheader("🎛 Interactive Filters")

st.caption(
    "Filter the dataset based on machine type and machine status."
)

col1, col2 = st.columns(2)

with col1:

    product_type = st.selectbox(
        "🏭 Machine Type",
        ["All"] + sorted(df["Type"].unique())
    )

with col2:

    failure_status = st.selectbox(
        "⚠ Machine Status",
        ["All", "Normal", "Failed"]
    )

filtered_df = df.copy()

if product_type != "All":
    filtered_df = filtered_df[
        filtered_df["Type"] == product_type
    ]

if failure_status == "Normal":
    filtered_df = filtered_df[
        filtered_df["Machine failure"] == 0
    ]

elif failure_status == "Failed":
    filtered_df = filtered_df[
        filtered_df["Machine failure"] == 1
    ]

st.info(f"📌 Showing **{len(filtered_df)}** records after applying filters.")

# ---------------------------------
# Distribution Analysis
# ---------------------------------

with st.container(border=True):

    section("📊 Distribution Analysis")

    st.caption(
        "Explore the distribution of machine status, machine type, rotational speed, and tool wear."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Machine Failure Distribution")

        fig, ax = create_chart("Machine Failure Distribution")

        sns.countplot(
            x=filtered_df["Machine failure"].map({0:"Normal",1:"Failed"}),
            palette=["#22C55E","#EF4444"],
            ax=ax,
            edgecolor="#E2E8F0",
            linewidth=0.5,
            alpha=0.85
        )

        ax.set_xlabel("Machine Status")
        ax.set_ylabel("Count")
        

        plt.tight_layout()

        st.pyplot(fig)

    with col2:

        st.markdown("### Machine Type Distribution")

        fig, ax = create_chart("Machine Type Distribution")

        sns.countplot(
            data=filtered_df,
            x="Type",
            palette="viridis",
            ax=ax,
            edgecolor="#E2E8F0",
            linewidth=0.5,
            alpha=0.85
        )

        ax.set_xlabel("Machine Type")
        ax.set_ylabel("Count")

        st.pyplot(fig)

    col3, col4 = st.columns(2)

    with col3:

        st.markdown("### Distribution of Rotational Speed")

        fig, ax = create_chart("Distribution of Rotational Speed")
        sns.histplot(
            filtered_df["Rotational speed [rpm]"],
            kde=True,
            color="#2563EB",
            edgecolor="#E2E8F0",
            linewidth=0.5,
            alpha=0.85,
            ax=ax
        )

        plt.tight_layout(pad=2)
        ax.set_xlabel("Rotational Speed (RPM)")

        st.pyplot(fig)

    with col4:

        st.markdown("### Distribution of Tool Wear")

        fig, ax = create_chart("Distribution of Tool Wear")

        sns.histplot(
            filtered_df["Tool wear [min]"],
            kde=True,
            color="#F59E0B",
            edgecolor="#E2E8F0",
            linewidth=0.5,
            alpha=0.85,
            ax=ax
        )

        plt.tight_layout(pad=2)

        ax.set_xlabel("Tool Wear (minutes)")

        st.pyplot(fig)



# ---------------------------------
# Relationship Analysis
# ---------------------------------

with st.container(border=True):

    section("🔗 Relationship Analysis")

    st.caption(
        "These visualizations highlight relationships between important machine parameters and machine failure."
    )

    # ---------------------------
    # Row 1
    # ---------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Relationship Between Rotational Speed and Torque")

        fig, ax = create_chart("Relationship Between Rotational Speed and Torque")

        sns.scatterplot(
            data=filtered_df,
            x="Rotational speed [rpm]",
            y="Torque [Nm]",
            hue="Machine failure",
            palette="Set1",
            color="#2563EB",
            alpha=0.7,
            s=45,
            ax=ax
        )

        plt.tight_layout(pad=2)
       

        ax.set_xlabel("Rotational Speed (RPM)")
        ax.set_ylabel("Torque (Nm)")
        ax.legend(title="Failure")

        st.pyplot(fig)

    with col2:

        st.markdown("### Relationship Between Air and Process Temperature")

        fig, ax = create_chart("Relationship Between Rotational Speed and Torque")

        sns.scatterplot(
            data=filtered_df,
            x="Air temperature [K]",
            y="Process temperature [K]",
            hue="Machine failure",
            palette="Set2",
            color="#2563EB",
            alpha=0.7,
            s=45,
            ax=ax
        )
        plt.tight_layout(pad=2)
        ax.set_xlabel("Air Temperature (K)")
        ax.set_ylabel("Process Temperature (K)")
        ax.legend(title="Failure")

        st.pyplot(fig)

    # ---------------------------
    # Row 2
    # ---------------------------

    col3, col4 = st.columns(2)

    with col3:

        st.markdown("### Tool Wear vs Machine Failure")

        fig, ax = create_chart("Relationship Between Rotational Speed and Torque")

        sns.boxplot(
            data=filtered_df,
            x="Machine failure",
            y="Tool wear [min]",
            palette="Set3",
            color="#60A5FA",
            linewidth=1,
            ax=ax
        )
        plt.tight_layout(pad=2)
        ax.set_xlabel("Machine Failure")
        ax.set_ylabel("Tool Wear (minutes)")

        st.pyplot(fig)

    with col4:

        st.markdown("### Torque vs Machine Failure")

        fig, ax = create_chart("Relationship Between Rotational Speed and Torque")

        sns.boxplot(
            data=filtered_df,
            x="Machine failure",
            y="Torque [Nm]",
            palette="Set2",
            color="#60A5FA",
            linewidth=1,
            ax=ax
        )
        plt.tight_layout(pad=2)
        ax.set_xlabel("Machine Failure")
        ax.set_ylabel("Torque (Nm)")

        st.pyplot(fig)



# ---------------------------------
# Failure Analysis
# ---------------------------------

with st.container(border=True):

    st.subheader("📋 Failure Analysis")

    st.caption(
        "Analyze the frequency and percentage contribution of different machine failure types."
    )

    failure_columns = ["TWF", "HDF", "PWF", "OSF", "RNF"]

    failure_counts = filtered_df[failure_columns].sum()

    # Consistent colors for both charts
    colors = [
        "#1E3A8A",  # Dark Blue
        "#2563EB",  # Royal Blue
        "#3B82F6",  # Blue
        "#60A5FA",  # Light Blue
        "#93C5FD"   # Lighter Blue
    ]

    col1, col2 = st.columns(2)

    # ---------------------------
    # Failure Distribution
    # ---------------------------

    with col1:

        st.markdown("### Failure Type Distribution")

        fig, ax = plt.subplots(figsize=(7, 5))

        sns.barplot(
            x=failure_counts.index,
            y=failure_counts.values,
            palette=colors,
            ax=ax
        )

        ax.set_xlabel("Failure Type")
        ax.set_ylabel("Count")

        st.pyplot(fig)

    # ---------------------------
    # Failure Percentage
    # ---------------------------

    with col2:

        st.markdown("### Failure Type Percentage")

        fig, ax = plt.subplots(figsize=(7, 5))

        ax.pie(
            failure_counts,
            labels=failure_counts.index,
            colors=colors,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.axis("equal")

        st.pyplot(fig)

# ---------------------------------
# Correlation Analysis
# ---------------------------------

with st.container(border=True):

    section("🔥 Correlation Analysis")

    st.caption(
        "The correlation analysis identifies relationships among numerical attributes and their influence on machine failure."
    )

    heatmap_columns = [

        "Air temperature [K]",
        "Process temperature [K]",
        "Rotational speed [rpm]",
        "Torque [Nm]",
        "Tool wear [min]",
        "Machine failure"

    ]

    correlation = filtered_df[heatmap_columns].corr()

    col1, col2 = st.columns(2)

    # ---------------------------
    # Heatmap
    # ---------------------------

    with col1:

        st.markdown("### Correlation Heatmap")

        fig, ax = plt.subplots(figsize=(7,5))

        sns.heatmap(
            correlation,
            annot=True,
            cmap="Blues",
            fmt=".2f",
            linewidths=0.5,
            square=True,
            ax=ax
        )

        st.pyplot(fig)

    # ---------------------------
    # Correlation with Failure
    # ---------------------------

    with col2:

        st.markdown("### Correlation with Machine Failure")

        corr_failure = (
            correlation["Machine failure"]
            .drop("Machine failure")
            .sort_values()
        )

        fig, ax = plt.subplots(figsize=(7,5))

        corr_failure.plot(
            kind="barh",
            color="teal",
            ax=ax
        )

        ax.set_xlabel("Correlation Coefficient")

        st.pyplot(fig)


# ---------------------------------
# Key Insights
# ---------------------------------

with st.container(border=True):

    section("💡 Key Insights")

    st.caption(
        "The following insights are automatically generated from the filtered dataset."
    )

    # ----------------------------
    # Calculate Metrics
    # ----------------------------

    failure_rate = (
        filtered_df["Machine failure"].mean() * 100
    )

    average_rpm = (
        filtered_df["Rotational speed [rpm]"].mean()
    )

    average_toolwear = (
        filtered_df["Tool wear [min]"].mean()
    )

    highest_corr = (
        corr_failure.abs().idxmax()
    )

    most_common_failure = (
        failure_counts.idxmax()
    )

    # ----------------------------
    # Metric Cards
    # ----------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📉 Failure Rate",
            f"{failure_rate:.2f}%"
        )

    with col2:
        st.metric(
            "⚙ Average RPM",
            f"{average_rpm:.0f}"
        )

    with col3:
        st.metric(
            "🛠 Average Tool Wear",
            f"{average_toolwear:.1f} min"
        )

    st.markdown("---")

    col4, col5 = st.columns(2)

    with col4:
        st.metric(
            "📈 Highest Correlated Feature",
            highest_corr
        )

    with col5:
        st.metric(
            "⚠ Most Frequent Failure",
            most_common_failure
        )

    st.markdown("---")

    st.subheader("📌 Dashboard Summary")

    st.success(f"""
✅ Total records analyzed: **{len(filtered_df)}**

✅ Overall machine failure rate: **{failure_rate:.2f}%**

✅ Most common failure type: **{most_common_failure}**

✅ Feature with the strongest relationship to machine failure: **{highest_corr}**

✅ Average rotational speed: **{average_rpm:.0f} RPM**

✅ Average tool wear: **{average_toolwear:.1f} minutes**
""")

    st.info("""
### 🎯 Recommendations

- Monitor machines with increasing **tool wear** to reduce unexpected failures.
- Regularly observe **torque** and **rotational speed** since they strongly influence machine performance.
- Track temperature readings to identify abnormal operating conditions.
- Use predictive maintenance strategies to minimize downtime and improve machine reliability.
""")