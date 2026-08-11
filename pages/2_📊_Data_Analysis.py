import streamlit as st
import pandas as pd
import numpy as np
from utils.ui import *
from utils.cards import *
from utils.charts import *
from utils.themes import *
load_css()
from utils.auth import require_login, hide_login_from_sidebar

require_login()
hide_login_from_sidebar()

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="Agentic FacilityOps AI",
    page_icon="🏭",
    layout="wide"
)

page_header(
    "📊",
    "Data Analysis",
    "Explore the AI4I Predictive Maintenance dataset through comprehensive EDA."
)
st.markdown("---")

# -------------------------
# Load Dataset
# -------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/ai4i2020.csv")

df = load_data()

# -------------------------
# Dataset Metrics
# -------------------------
st.subheader("Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Rows", df.shape[0])

with col2:
    st.metric("Columns", df.shape[1])

with col3:
    st.metric("Missing Values", df.isnull().sum().sum())

with col4:
    st.metric("Duplicate Rows", df.duplicated().sum())

st.markdown("---")

# -------------------------
# Dataset Preview
# -------------------------
st.subheader("Dataset Preview")

preview_option = st.radio(
    "Select",
    ["First 5 Rows", "Last 5 Rows", "Random 5 Rows", "All Records"],
    horizontal=True
)

if preview_option == "First 5 Rows":

    st.dataframe(
        df.head(),
        use_container_width=True
    )

elif preview_option == "Last 5 Rows":

    st.dataframe(
        df.tail(),
        use_container_width=True
    )

elif preview_option == "Random 5 Rows":

    st.dataframe(
        df.sample(5),
        use_container_width=True
    )

elif preview_option == "All Records":

    st.dataframe(
        df,
        use_container_width=True,
        height=250
    )

st.markdown("---")

# -------------------------
# Dataset Information
# -------------------------
st.subheader("Dataset Information")

col1, col2 = st.columns(2)

with col1:
    st.write("### Shape")
    st.write(df.shape)

    st.write("### Data Types")
    st.dataframe(df.dtypes.astype(str))

with col2:
    st.write("### Missing Values")
    st.dataframe(df.isnull().sum().to_frame("Missing Values"))

    st.write("### Duplicate Rows")
    st.write(df.duplicated().sum())

st.markdown("---")

# -------------------------
# Descriptive Statistics
# -------------------------
st.subheader("Descriptive Statistics")

st.dataframe(df.describe(), use_container_width=True)

st.markdown("---")

# -------------------------
# Numeric Columns
# -------------------------
st.subheader("Numeric Columns")

numeric_df = df.select_dtypes(include=np.number)

st.dataframe(numeric_df.head(), use_container_width=True)

st.success("Data Analysis Completed Successfully ✅")