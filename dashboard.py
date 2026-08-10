import streamlit as st
import plotly.express as px

def show_dashboard(filtered_df, status_option):
    st.markdown("""
        <div style=" padding: 25px; border-radius: 18px; text-align: center; color: green; margin-bottom: 20px;">
            <h1 style="color:Black; margin:0;">🏭 AI4I Predictive Maintenance Dashboard</h1>
            <p style="font-size:20px; opacity: 0.95; margin-top:6px;">Real-time asset telemetry monitoring, failure diagnostics, and maintenance insights.</p>
        </div>
    """, unsafe_allow_html=True)

    total_machines = len(filtered_df)
    machine_failures = int((filtered_df["Machine failure"] == 1).sum())
    healthy_machines = int((filtered_df["Machine failure"] == 0).sum())
    fail_rate = (machine_failures / total_machines * 100) if total_machines > 0 else 0

    st.subheader(f" Fleet KPI Summary — `{status_option}`")

    c1, c2, c3 = st.columns(3)
    c1.metric("🏭 Filtered Machines", f"{total_machines:,}")
    c2.metric("⚠️ Machine Failures", f"{machine_failures:,}")
    c3.metric("✅ Healthy Machines", f"{healthy_machines:,}")

    c4, c5 = st.columns(2)
    avg_rpm = filtered_df['Rotational speed [rpm]'].mean() if total_machines > 0 else 0
    c4.metric("⚙️ Avg Rotational Speed", f"{avg_rpm:.2f} RPM")
    c5.metric("📉 Active Subset Failure Rate", f"{fail_rate:.2f}%")

    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        fig = px.histogram(filtered_df, x="Machine failure", color="Machine failure", title="Machine Failure Breakdown", color_discrete_sequence=["#10b981", "#ef4444"])
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        fig = px.histogram(filtered_df, x="Type", color="Type", title="Distribution by Machine Type", color_discrete_sequence=px.colors.qualitative.Vivid)
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.scatter(filtered_df, x="Rotational speed [rpm]", y="Torque [Nm]", color="Machine failure", title="RPM vs. Torque Correlation", color_continuous_scale="Turbo")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.box(filtered_df, x="Type", y="Tool wear [min]", color="Type", title="Tool Wear (min) by Machine Type")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Filtered Dataset")
    st.dataframe(filtered_df)