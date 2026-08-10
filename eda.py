import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def show_eda(df):
    st.markdown("""
        <div style="padding: 22px; border-radius: 18px; text-align: center; color: green; margin-bottom: 20px; border: 1px solid rgba(255, 255, 255, 0.1);">
            <h1 style="color:black; margin:0;">📊 Exploratory Data Analysis (EDA)</h1>
            <p style="font-size:15px; opacity:0.95; margin-top:6px;">Deep statistical inspection, feature correlations, and distribution metrics.</p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("📋 Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.info(f"**Dataset Shape:** `{df.shape[0]}` rows × `{df.shape[1]}` columns")
    with c2:
        st.subheader("Missing Values")
        st.dataframe(df.isnull().sum(), use_container_width=True)

    st.markdown("---")

    st.subheader("📈 Descriptive Statistics")
    st.dataframe(df.describe(), use_container_width=True)

    num = df.select_dtypes(include="number")

    st.markdown("---")

    st.subheader("🔥 Correlation Heatmap")
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')

    sns.heatmap(num.corr(), annot=True, cmap="mako", fmt=".2f", ax=ax, cbar=True)
    st.pyplot(fig)

    st.markdown("---")

    st.subheader("📊 Feature Distributions")
    for col in num.columns:
        fig_hist = px.histogram(df, x=col, title=f"{col} Distribution", template="plotly_dark", color_discrete_sequence=["#3b82f6"])
        fig_hist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("---")

    st.subheader("📦 Feature Outliers & Range (Box Plots)")
    box_cols = ["Air temperature [K]", "Process temperature [K]", "Rotational speed [rpm]", "Torque [Nm]", "Tool wear [min]"]
    for col in box_cols:
        if col in df.columns:
            fig_box = px.box(df, y=col, title=f"{col} Box Plot", template="plotly_dark", color_discrete_sequence=["#8b5cf6"])
            fig_box.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")

    if "Machine failure" in df.columns:
        st.subheader("🚨 Machine Failure Breakdown")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            fig_fail_hist = px.histogram(df, x="Machine failure", color="Machine failure", template="plotly_dark", color_discrete_map={0: "#10b981", 1: "#ef4444"})
            fig_fail_hist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_fail_hist, use_container_width=True)
        
        with col_f2:
            fig_pie = px.pie(df, names="Machine failure", title="Failure Percentage", template="plotly_dark", color_discrete_sequence=["#10b981", "#ef4444"])
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pie, use_container_width=True)

    if "Type" in df.columns:
        st.subheader("🏭 Machine Type Distribution")
        fig_type = px.histogram(df, x="Type", color="Type", template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_type.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_type, use_container_width=True)

    if all(c in df.columns for c in ["Rotational speed [rpm]", "Torque [Nm]", "Machine failure"]):
        st.subheader("⚙️ Speed vs Torque Analysis")
        fig_scatter = px.scatter(
            df, 
            x="Rotational speed [rpm]", 
            y="Torque [Nm]", 
            color="Machine failure",
            template="plotly_dark",
            color_continuous_scale="Turbo"
        )
        fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_scatter, use_container_width=True)

    if "Machine failure" in num.columns:
        corr = num.corr()["Machine failure"].sort_values()
        st.subheader("🎯 Feature Correlation with Machine Failure")
        fig_corr = px.bar(
            x=corr.index, 
            y=corr.values,
            labels={"x": "Feature", "y": "Correlation Coefficient"},
            template="plotly_dark",
            color_discrete_sequence=["#ec4899"]
        )
        fig_corr.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_corr, use_container_width=True)