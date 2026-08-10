import streamlit as st

def show_machine_explorer(df, filtered_df):
    st.markdown("""
        <div style="padding: 22px; border-radius: 18px; text-align: center; color: Blue; margin-bottom: 20px;">
            <h1 style="color:black; margin:0;">🔍 Individual Machine Explorer</h1>
            <p style="font-size:15px; opacity:0.95; margin-top:6px;">Select a Product ID to review telemetry parameters, sensor metrics, and operational details.</p>
        </div>
    """, unsafe_allow_html=True)

    explorer_ids = sorted(filtered_df["Product ID"].astype(str).unique()) if len(filtered_df) > 0 else sorted(df["Product ID"].astype(str).unique())
    
    product_id = st.selectbox(
        "🔍 Search / Select Product ID",
        options=explorer_ids,
        index=0 if explorer_ids else None
    )

    if st.button("Inspect Machine"):
        machine = df[df["Product ID"].astype(str) == product_id.strip()]
        if machine.empty:
            st.error("Product ID not found!")
            st.session_state.selected_machine = None
        else:
            st.session_state.selected_machine = machine.iloc[0]

    if st.session_state.get("selected_machine") is not None:
        row = st.session_state.selected_machine

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📌 Machine Information")
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Product ID:** `{row['Product ID']}`")
            st.write(f"**Machine Type:** `{row['Type']}`")
        with c2:
            st.write(f"**Air Temperature:** `{row['Air temperature [K]']} K`")
            st.write(f"**Process Temperature:** `{row['Process temperature [K]']} K`")

        st.markdown("---")

        st.subheader("📡 Live Sensor Values")
        s1, s2, s3, s4, s5 = st.columns(5)
        s1.metric("🌡 Air Temp", f"{row['Air temperature [K]']} K")
        s2.metric("🔥 Process Temp", f"{row['Process temperature [K]']} K")
        s3.metric("⚙ Speed", f"{int(row['Rotational speed [rpm]'])} RPM")
        s4.metric("🔩 Torque", f"{row['Torque [Nm]']} Nm")
        s5.metric("🛠 Tool Wear", f"{row['Tool wear [min]']} min")

        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader("⚠ Failure Analysis Indicators")
        failures = {
            "Tool Wear Failure (TWF)": row["TWF"],
            "Heat Dissipation Failure (HDF)": row["HDF"],
            "Power Failure (PWF)": row["PWF"],
            "Overstrain Failure (OSF)": row["OSF"],
            "Random Failure (RNF)": row["RNF"]
        }

        f_cols = st.columns(5)
        for idx, (name, value) in enumerate(failures.items()):
            with f_cols[idx]:
                if value == 1:
                    st.error(f"❌ {name}")
                else:
                    st.success(f"✅ {name}")