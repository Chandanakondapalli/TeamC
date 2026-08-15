import streamlit as st
from auth import require_admin
require_admin()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Exploratory Data Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊Exploratory Data Analysis")

st.markdown(
"""
This module performs Exploratory Data Analysis (EDA) on the
AI4I 2020 Predictive Maintenance dataset.
"""
)


df = pd.read_csv("dataset/ai4i2020.csv")

st.markdown("---")

st.subheader("Dataset Preview")

col1, col2 = st.columns(2)

with col1:
    st.write("### First 5 Rows")
    st.dataframe(df.head(), width="stretch")

with col2:
    st.write("### Last 5 Rows")
    st.dataframe(df.tail(), width="stretch")

    st.markdown("---")

st.subheader("Dataset Information")

col1, col2, col3 = st.columns(3)

col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Missing Values", int(df.isnull().sum().sum()))

st.write("### Column Names")

st.write(df.columns.tolist())

st.markdown("---")

st.subheader("Statistical Summary")

st.dataframe(df.describe(), width="stretch")

st.markdown("---")

st.subheader("Missing Values")

missing = df.isnull().sum().to_frame()

missing.columns = ["Missing Values"]

st.dataframe(missing, width="stretch")

st.markdown("---")

st.subheader("Correlation Matrix")

corr = df.corr(numeric_only=True)

st.dataframe(corr, width="stretch")

st.markdown("---")

st.subheader("Correlation Heatmap")

fig, ax = plt.subplots(figsize=(10,8))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    ax=ax
)

st.pyplot(fig)

st.markdown("---")

st.success("✅ Exploratory Data Analysis Completed Successfully")


# .\.venv\Scripts\Activate.ps1
# pip install reportlab
# python -m streamlit run Home.py

