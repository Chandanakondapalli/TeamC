import streamlit as st


# ----------------------------------------
# KPI Card
# ----------------------------------------

def kpi_card(icon, title, value, subtitle):

    st.markdown(f"""
    <div class="kpi-card">

        <div class="kpi-icon">
            {icon}
        </div>

        <div class="kpi-title">
            {title}
        </div>

        <div class="kpi-value">
            {value}
        </div>

        <div class="kpi-subtitle">
            {subtitle}
        </div>

    </div>
    """, unsafe_allow_html=True)


# ----------------------------------------
# Info Card
# ----------------------------------------

def info_card(title, text):

    st.markdown(f"""
    <div class="info-card">

        <h3>{title}</h3>

        <p>{text}</p>

    </div>
    """, unsafe_allow_html=True)