import io
import re
import streamlit as st
from fpdf import FPDF


class MachineReportPDF(FPDF):

  def header(self):
    self.set_font("Helvetica", "B", 16)
    self.set_text_color(15, 23, 42)
    self.cell(
        0, 10, "Individual Machine Inspection Report", border=False, ln=True
    )
    self.set_font("Helvetica", "I", 10)
    self.set_text_color(100, 116, 139)
    self.cell(
        0, 6, "Industrial AI FacilityOps Monitoring System", border=False, ln=True
    )
    self.set_draw_color(226, 232, 240)
    self.line(10, 28, 200, 28)
    self.ln(8)

  def footer(self):
    self.set_y(-15)
    self.set_font("Helvetica", "I", 8)
    self.set_text_color(148, 163, 184)
    self.cell(0, 10, f"Page {self.page_no()}", align="C")


def clean_markdown(text):
  """Removes markdown syntax (bold, headers, bullets) for FPDF compatibility."""
  if not text:
    return ""
  # Clean bold/italic markdown signs
  text = re.sub(r"\*\*|\*", "", text)
  # Replace markdown headers (e.g. ## Header -> Header)
  text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
  return text


def create_machine_pdf(row, ai_report_text=None):
  pdf = MachineReportPDF()
  pdf.add_page()

  # 1. Machine Information
  pdf.set_font("Helvetica", "B", 12)
  pdf.set_text_color(30, 41, 59)
  pdf.cell(0, 8, "1. Machine Information", ln=True)
  pdf.ln(2)

  pdf.set_font("Helvetica", "", 10)
  pdf.set_fill_color(241, 245, 249)

  info_data = [
      ("Product ID:", str(row["Product ID"]), "Machine Type:", str(row["Type"])),
      (
          "Air Temperature:",
          f"{row['Air temperature [K]']} K",
          "Process Temperature:",
          f"{row['Process temperature [K]']} K",
      ),
  ]

  for item in info_data:
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(45, 7, item[0], border=1, fill=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(50, 7, item[1], border=1)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(45, 7, item[2], border=1, fill=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(50, 7, item[3], border=1, ln=True)

  pdf.ln(6)

  # 2. Live Sensor Telemetry
  pdf.set_font("Helvetica", "B", 12)
  pdf.cell(0, 8, "2. Live Sensor Telemetry", ln=True)
  pdf.ln(2)

  pdf.set_font("Helvetica", "B", 9)
  pdf.set_fill_color(226, 232, 240)
  pdf.cell(38, 7, "Air Temp (K)", border=1, fill=True, align="C")
  pdf.cell(38, 7, "Process Temp (K)", border=1, fill=True, align="C")
  pdf.cell(38, 7, "Speed (RPM)", border=1, fill=True, align="C")
  pdf.cell(38, 7, "Torque (Nm)", border=1, fill=True, align="C")
  pdf.cell(38, 7, "Tool Wear (min)", border=1, fill=True, align="C")
  pdf.ln()

  pdf.set_font("Helvetica", "", 9)
  pdf.cell(38, 7, str(row["Air temperature [K]"]), border=1, align="C")
  pdf.cell(38, 7, str(row["Process temperature [K]"]), border=1, align="C")
  pdf.cell(
      38, 7, str(int(row["Rotational speed [rpm]"])), border=1, align="C"
  )
  pdf.cell(38, 7, str(row["Torque [Nm]"]), border=1, align="C")
  pdf.cell(38, 7, str(row["Tool wear [min]"]), border=1, align="C")
  pdf.ln(10)

  # 3. Failure Indicators
  pdf.set_font("Helvetica", "B", 12)
  pdf.cell(0, 8, "3. Failure Analysis Indicators", ln=True)
  pdf.ln(2)

  failures = {
      "Tool Wear Failure (TWF)": row["TWF"],
      "Heat Dissipation Failure (HDF)": row["HDF"],
      "Power Failure (PWF)": row["PWF"],
      "Overstrain Failure (OSF)": row["OSF"],
      "Random Failure (RNF)": row["RNF"],
  }

  for name, val in failures.items():
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(120, 7, name, border=1)
    if val == 1:
      pdf.set_text_color(220, 38, 38)
      pdf.set_font("Helvetica", "B", 10)
      pdf.cell(70, 7, "FAILED (1)", border=1, align="C", ln=True)
    else:
      pdf.set_text_color(22, 163, 74)
      pdf.set_font("Helvetica", "", 10)
      pdf.cell(70, 7, "NORMAL (0)", border=1, align="C", ln=True)
    pdf.set_text_color(0, 0, 0)

  pdf.ln(10)

  # 4. Llama 3.2 AI Diagnostic Section
  pdf.set_font("Helvetica", "B", 12)
  pdf.set_text_color(30, 41, 59)
  pdf.cell(0, 8, "4. AI Predictive Diagnostic Report (Llama 3.2)", ln=True)
  pdf.ln(2)

  if ai_report_text:
    cleaned_report = clean_markdown(ai_report_text)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_fill_color(248, 250, 252)
    pdf.multi_cell(
        0,
        6,
        cleaned_report,
        border=1,
        fill=True,
        markdown=False,
    )
  else:
    pdf.set_font("Helvetica", "I", 9.5)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(
        0,
        8,
        "No AI Diagnostic report generated yet. Run analysis in AI Predictive Diagnostic module.",
        border=1,
        ln=True,
    )

  buffer = io.BytesIO()
  pdf.output(buffer)
  buffer.seek(0)
  return buffer.getvalue()


def show_machine_explorer(df, filtered_df):
  st.markdown(
      """
        <div style="padding: 22px; border-radius: 18px; text-align: center; color: Blue; margin-bottom: 20px;">
            <h1 style="color:black; margin:0;">🔍 Individual Machine Explorer</h1>
            <p style="font-size:15px; opacity:0.95; margin-top:6px;">Select a Product ID to review telemetry parameters, sensor metrics, and operational details.</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  explorer_ids = (
      sorted(filtered_df["Product ID"].astype(str).unique())
      if len(filtered_df) > 0
      else sorted(df["Product ID"].astype(str).unique())
  )

  product_id = st.selectbox(
      "🔍 Search / Select Product ID",
      options=explorer_ids,
      index=0 if explorer_ids else None,
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
      st.write(
          f"**Process Temperature:** `{row['Process temperature [K]']} K`"
      )

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
        "Random Failure (RNF)": row["RNF"],
    }

    f_cols = st.columns(5)
    for idx, (name, value) in enumerate(failures.items()):
      with f_cols[idx]:
        if value == 1:
          st.error(f"❌ {name}")
        else:
          st.success(f"✅ {name}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # Retrieve AI Diagnostic Report from session_state if available for this specific Product ID
    ai_report_content = None
    if (
        st.session_state.get("ai_report") is not None
        and st.session_state.get("ai_report_product_id") == row["Product ID"]
    ):
      ai_report_content = st.session_state.ai_report

    st.subheader("📄 Export Inspection Report")
    if ai_report_content:
      st.success("✅ AI Diagnostic Report included in PDF payload.")
    else:
      st.info(
          "💡 Tip: Generate a diagnostic report in 'AI Predictive Diagnostic'"
          " module to include full AI recommendations in this PDF."
      )

    pdf_bytes = create_machine_pdf(row, ai_report_text=ai_report_content)

    st.download_button(
        label=f"📥 Download PDF Report ({row['Product ID']})",
        data=pdf_bytes,
        file_name=f"Machine_Report_{row['Product ID']}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )