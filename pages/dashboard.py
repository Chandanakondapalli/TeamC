import streamlit as st
import pandas as pd
import plotly.express as px
from auth import require_admin
require_admin()

st.set_page_config(
    page_title="Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈Interactive Dashboard")

st.markdown("""
This dashboard provides an interactive visualization of the
AI4I Predictive Maintenance Dataset.
""")


df = pd.read_csv("dataset/ai4i2020.csv")

st.sidebar.header("Filters")

machine = st.sidebar.multiselect(
    "Machine Type",
    options=df["Type"].unique(),
    default=df["Type"].unique()
)

failure = st.sidebar.multiselect(
    "Machine Failure",
    options=df["Machine failure"].unique(),
    default=df["Machine failure"].unique()
)

filtered_df = df[
    (df["Type"].isin(machine)) &
    (df["Machine failure"].isin(failure))
]


st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Machines",
    len(filtered_df)
)

col2.metric(
    "Failures",
    int(filtered_df["Machine failure"].sum())
)

col3.metric(
    "Average RPM",
    round(filtered_df["Rotational speed [rpm]"].mean(),2)
)

col4.metric(
    "Average Torque",
    round(filtered_df["Torque [Nm]"].mean(),2)
)
st.markdown("---")

st.subheader("Dataset Preview")

st.dataframe(
    filtered_df,
    width="stretch"
)
st.markdown("---")

st.subheader("Machine Failure Distribution")

fig = px.pie(
    filtered_df,
    names="Machine failure",
    title="Machine Failure Distribution"
)

st.plotly_chart(
    fig,
    width="stretch"
)
st.markdown("---")

st.subheader("Machine Type Distribution")

fig = px.bar(
    filtered_df,
    x="Type",
    color="Type",
    title="Machine Type Distribution"
)

st.plotly_chart(fig, width="stretch")
st.markdown("---")

st.subheader("Rotational Speed Analysis")

fig = px.histogram(
    filtered_df,
    x="Rotational speed [rpm]",
    nbins=30,
    title="Rotational Speed Distribution"
)

st.plotly_chart(fig, width="stretch")
st.markdown("---")

st.subheader("Tool Wear Analysis")

fig = px.box(
    filtered_df,
    y="Tool wear [min]",
    color="Type",
    title="Tool Wear by Machine Type"
)

st.plotly_chart(fig, width="stretch")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    fig = px.scatter(
        filtered_df,
        x="Air temperature [K]",
        y="Process temperature [K]",
        color="Type",
        title="Air vs Process Temperature"
    )

    st.plotly_chart(fig, width="stretch")

with col2:

    fig = px.scatter(
        filtered_df,
        x="Rotational speed [rpm]",
        y="Torque [Nm]",
        color="Machine failure",
        title="RPM vs Torque"
    )

    st.plotly_chart(fig, width="stretch")
    st.markdown("---")

st.subheader("Dashboard Summary")

st.success(f"""
Total Machines : {len(filtered_df)}

Machine Failures : {filtered_df['Machine failure'].sum()}

Average Air Temperature :
{filtered_df['Air temperature [K]'].mean():.2f} K

Average Process Temperature :
{filtered_df['Process temperature [K]'].mean():.2f} K

Average RPM :
{filtered_df['Rotational speed [rpm]'].mean():.2f}

Average Torque :
{filtered_df['Torque [Nm]'].mean():.2f}

Average Tool Wear :
{filtered_df['Tool wear [min]'].mean():.2f}
""")