import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

# Custom Utility Imports
from utils.ui import page_header, load_css
from utils.database import *
from utils.cards import *
from utils.auth import require_login, hide_login_from_sidebar

require_login()
hide_login_from_sidebar()

# ---------------------------------
# Page Configuration
# ---------------------------------
st.set_page_config(
    page_title="Machine Explorer | Agentic FacilityOps",
    page_icon="🔍",
    layout="wide"
)
load_css()

# ---------------------------------
# Data Loading & Logic
# ---------------------------------
@st.cache_data
def load_data():
    file_path = "data/ai4i2020.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame()

df = load_data()

# Helper: Calculate Percentile Ranking
def get_rank_context(column, value):
    if df.empty: return 0
    return (df[column] < value).mean() * 100

# Persistent State for Selected Machine
if "selected_m" not in st.session_state:
    st.session_state.selected_m = None

# ---------------------------------
# Header Section
# ---------------------------------
page_header(
    "🔍", 
    "Machine Explorer", 
    "Perform deep-dive audits, analyze sensor anomalies, and evaluate machine health."
)

# ---------------------------------
# SEARCH BAR: Search by Product ID
# ---------------------------------
with st.container(border=True):
    col_search, col_btn, col_reset = st.columns([3, 1, 1])
    with col_search:
        product_id = st.selectbox(
            "Search Machine by Product ID",
            options=[""] + sorted(df["Product ID"].unique()) if not df.empty else [""],
            format_func=lambda x: "Select Product ID..." if x == "" else x,
            index=0,
            label_visibility="collapsed"
        )
    with col_btn:
        if st.button("Inspect Machine", use_container_width=True, type="primary"):
            if product_id:
                st.session_state.selected_m = df[df["Product ID"] == product_id].iloc[0]
            else:
                st.warning("Please select a Product ID")
    with col_reset:
        if st.button("Clear Explorer", use_container_width=True):
            st.session_state.selected_m = None
            st.rerun()

st.divider()

# ---------------------------------
# MAIN EXPLORER CONTENT
# ---------------------------------
if st.session_state.selected_m is not None:
    m = st.session_state.selected_m

    # --- SECTION 1: MACHINE INFORMATION & METADATA ---
    st.subheader("📄 Machine Information")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.write("**Product Identity**")
        st.write(f"ID: `{m['Product ID']}`")
        st.write(f"UDI: `{int(m['UDI'])}`")
    with c2:
        st.write("**Machine Specifications**")
        st.write(f"Type: `{m['Type']}` (Quality Class)")
        st.write(f"Series: 2020-AI-Standard")
    with c3:
        st.write("**Operational Status**")
        status = "🔴 FAILED" if m['Machine failure'] == 1 else "🟢 NORMAL"
        st.write(f"Current State: **{status}**")
    with c4:
        st.write("**Maintenance Priority**")
        prio = "IMMEDIATE" if m['Machine failure'] == 1 else ("HIGH" if m['Tool wear [min]'] > 180 else "LOW")
        st.write(f"Priority Level: `{prio}`")

    # --- SECTION 2: LIVE SENSOR VALUES (With Context) ---
    st.markdown("### 📡 Live Sensor Diagnostics")
    st.caption("Real-time telemetry and fleet-wide percentile ranking.")
    
    sc1, sc2, sc3, sc4, sc5 = st.columns(5)
    
    # Sensor 1: Air Temp
    sc1.metric("Air Temperature", f"{m['Air temperature [K]']:.1f} K", 
               f"{get_rank_context('Air temperature [K]', m['Air temperature [K]']):.0f}% Rank")
    # Sensor 2: Process Temp
    sc2.metric("Process Temp", f"{m['Process temperature [K]']:.1f} K", 
               f"{get_rank_context('Process temperature [K]', m['Process temperature [K]']):.0f}% Rank")
    # Sensor 3: Speed
    sc3.metric("Rotational Speed", f"{int(m['Rotational speed [rpm]'])} RPM", 
               f"{get_rank_context('Rotational speed [rpm]', m['Rotational speed [rpm]']):.0f}% Rank")
    # Sensor 4: Torque
    sc4.metric("Torque", f"{m['Torque [Nm]']:.1f} Nm", 
               f"{get_rank_context('Torque [Nm]', m['Torque [Nm]']):.0f}% Rank")
    # Sensor 5: Tool Wear
    sc5.metric("Tool Wear", f"{m['Tool wear [min]']} min", 
               f"{get_rank_context('Tool wear [min]', m['Tool wear [min]']):.0f}% Rank", delta_color="inverse")

    # --- SECTION 3: HEALTH STATUS & RISK SCORING ---
    st.divider()
    st.subheader("❤️ Health Status & Risk Scoring")
    
    col_h1, col_h2 = st.columns([1, 2])
    
    with col_h1:
        # Calculate a dynamic Health Score
        health_score = 100
        if m["Machine failure"] == 1: health_score = 20
        elif m["Tool wear [min]"] > 200: health_score = 50
        elif m["Tool wear [min]"] > 150: health_score = 75
        
        st.metric("Aggregate Health Score", f"{health_score}%")
        st.progress(health_score / 100)
        
        if health_score < 40: st.error("Critical Condition: Immediate attention required.")
        elif health_score < 80: st.warning("Warning: Maintenance scheduled soon.")
        else: st.success("Healthy: Machine operating within optimal bounds.")

    with col_h2:
        # Radar Chart for Performance "Fingerprint"
        feats = ["Air temperature [K]", "Process temperature [K]", "Rotational speed [rpm]", "Torque [Nm]", "Tool wear [min]"]
        labels = ["Air", "Process", "Speed", "Torque", "Wear"]
        # Normalize for chart
        m_norm = [(m[f] - df[f].min()) / (df[f].max() - df[f].min()) for f in feats]
        avg_norm = [(df[f].mean() - df[f].min()) / (df[f].max() - df[f].min()) for f in feats]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=m_norm, theta=labels, fill='toself', name='Current Machine', line_color='#008375'))
        fig_radar.add_trace(go.Scatterpolar(r=avg_norm, theta=labels, fill='toself', name='Fleet Average', line_color='#94a3b8'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False)), height=350, margin=dict(l=50, r=50, t=20, b=20))
        st.plotly_chart(fig_radar, use_container_width=True)

    # --- SECTION 4: FAILURE ANALYSIS ---
    st.divider()
    st.subheader("⚠️ Failure Analysis")
    
    # Map binary failure columns to descriptions
    failure_types = {
        "TWF": ("Tool Wear Failure", "The cutting tool has reached its physical wear limit."),
        "HDF": ("Heat Dissipation Failure", "The process temperature difference exceeded 8.6K."),
        "PWF": ("Power Failure", "The power (Torque * Speed) dropped below 3500W or exceeded 9000W."),
        "OSF": ("Overstrain Failure", "The product of Tool Wear and Torque exceeded limits."),
        "RNF": ("Random Failure", "A non-deterministic anomaly detected in the sensor stream.")
    }
    
    detected = [details for code, details in failure_types.items() if m[code] == 1]
    
    if not detected:
        st.success("Analysis Complete: No specific failure modes detected in historical logs.")
    else:
        st.error(f"Alert: {len(detected)} Failure Mode(s) identified.")
        for title, desc in detected:
            with st.expander(f"🔴 {title}", expanded=True):
                st.write(desc)

    # --- SECTION 5: FLEET BENCHMARKING (Interactive Histogram) ---
    st.divider()
    st.subheader("📊 Fleet Benchmarking")
    st.write("Understand this machine's performance relative to the entire facility.")
    
    feat_choice = st.selectbox("Select metric for distribution analysis:", 
                              ["Torque [Nm]", "Rotational speed [rpm]", "Tool wear [min]"])
    
    fig_hist = px.histogram(df, x=feat_choice, nbins=50, color_discrete_sequence=['#cbd5e1'])
    fig_hist.add_vline(x=m[feat_choice], line_width=4, line_dash="dash", line_color="#ef4444")
    fig_hist.add_annotation(x=m[feat_choice], text="Selected Unit", showarrow=True, arrowhead=1)
    fig_hist.update_layout(height=300, template="plotly_white", margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_hist, use_container_width=True)

    # --- SECTION 6: AI ACTION BRIDGE ---
    st.divider()
    with st.container(border=True):
        ac1, ac2 = st.columns([3, 1])
        with ac1:
            st.markdown("### 🤖 Open AI Maintenance Assistant")
            st.write("Generate a comprehensive maintenance roadmap, including cost estimation and scheduled downtime windows based on the data above.")
        with ac2:
            st.write(" ") # Spacer
            if st.button("Generate AI Report", use_container_width=True, type="primary"):
                st.session_state.selected_machine_id = m["Product ID"]
                st.session_state.open_from_explorer = True
                st.switch_page("pages/4_🤖_AI_Maintenance_Assistant.py")

else:
    # --- EMPTY STATE: FLEET OVERVIEW ---
    st.info("👈 Please select a Machine Product ID and click 'Inspect' to begin.")
    
    st.subheader("Fleet Summary")
    f_c1, f_c2, f_c3 = st.columns(3)
    f_c1.metric("Total Monitored Assets", len(df))
    f_c2.metric("Fleet Health Index", f"{(1 - df['Machine failure'].mean())*100:.1f}%")
    f_c3.metric("Critical Alerts", len(df[df['Machine failure'] == 1]))
    
    st.markdown("#### Operational Trends (Failures by Type)")
    type_chart = df.groupby('Type')['Machine failure'].mean() * 100
    st.bar_chart(type_chart)