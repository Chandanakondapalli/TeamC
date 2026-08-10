import streamlit as st
import pandas as pd
import io
from datetime import date, timedelta
from database import get_work_orders, add_work_order, update_work_order_status, delete_work_order

# ReportLab imports for PDF generation
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_next_wo_id(wo_df):
    """Generates a non-conflicting Work Order ID even if records are deleted."""
    if wo_df.empty or "wo_id" not in wo_df.columns:
        return "WO-2026-001"
    
    extracted_ids = wo_df["wo_id"].str.extract(r'(\d+)$')[0].dropna()
    if not extracted_ids.empty:
        max_id = extracted_ids.astype(int).max()
        return f"WO-2026-{max_id + 1:03d}"
    
    return f"WO-2026-{len(wo_df) + 1:03d}"

def convert_df_to_excel(df_to_convert):
    """Converts a DataFrame to an Excel byte stream for downloading."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_to_convert.to_excel(writer, index=False, sheet_name='Work_Orders')
    return output.getvalue()

def convert_df_to_pdf(df_to_convert):
    """Converts a DataFrame to a styled PDF byte stream using ReportLab."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=landscape(letter), 
        rightMargin=20, 
        leftMargin=20, 
        topMargin=20, 
        bottomMargin=20
    )
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f172a'),
        alignment=1, # Center
        spaceAfter=15
    )
    
    # Title
    elements.append(Paragraph("<b>Maintenance Work Orders Report</b>", title_style))
    elements.append(Spacer(1, 10))
    
    # Table Data Assembly
    headers = [str(col).upper().replace('_', ' ') for col in df_to_convert.columns]
    
    # Define cell style for word wrap
    cell_style = ParagraphStyle('CellStyle', fontSize=8, leading=10)
    header_style = ParagraphStyle('HeaderStyle', fontSize=9, leading=11, textColor=colors.white, fontName="Helvetica-Bold")
    
    table_data = []
    # Add Header Row
    table_data.append([Paragraph(h, header_style) for h in headers])
    
    # Add Data Rows
    for _, row in df_to_convert.iterrows():
        row_cells = []
        for val in row:
            row_cells.append(Paragraph(str(val), cell_style))
        table_data.append(row_cells)
    
    # Create Table
    pdf_table = Table(table_data, repeatRows=1)
    pdf_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    
    elements.append(pdf_table)
    doc.build(elements)
    
    return buffer.getvalue()

def show_work_orders_hub(df):
    st.markdown("""
        <div style="padding: 22px; border-radius: 18px; text-align: center; color: green; margin-bottom: 20px;">
            <h1 style="color:black; margin:0;">🛠️ Maintenance Work Orders Hub</h1>
            <p style="font-size:15px; opacity:0.95; margin-top:6px;">Create, manage, search, update, track, and export maintenance records with SQLite storage.</p>
        </div>
    """, unsafe_allow_html=True)

    # 1. KPI CARDS
    wo_df = get_work_orders()

    st.subheader("📊 Work Order Metrics & KPIs")
    total_wo = len(wo_df)
    
    if total_wo > 0 and "status" in wo_df.columns and "priority" in wo_df.columns:
        open_wo = len(wo_df[wo_df["status"] == "Open"])
        assigned_wo = len(wo_df[wo_df["status"] == "Assigned"])
        in_progress_wo = len(wo_df[wo_df["status"] == "In Progress"])
        completed_wo = len(wo_df[wo_df["status"] == "Completed"])
        critical_wo = len(wo_df[wo_df["priority"] == "Critical"])
    else:
        open_wo = assigned_wo = in_progress_wo = completed_wo = critical_wo = 0

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("📋 Total Tickets", total_wo)
    k2.metric("🟡 Open / Assigned", open_wo + assigned_wo)
    k3.metric("🔵 In Progress", in_progress_wo)
    k4.metric("🟢 Completed", completed_wo)
    k5.metric("🔴 Critical Priority", critical_wo)

    st.markdown("---")

    # 2. CREATE WORK ORDER FORM (MODULE 5)
    st.subheader("📝 Module 5: Create Maintenance Work Order")

    all_product_ids = sorted(df["Product ID"].astype(str).unique()) if not df.empty and "Product ID" in df.columns else ["N/A"]
    selected_product_id = all_product_ids[0]
    default_issue = "Routine Maintenance Inspection"
    default_priority_index = 1

    if st.session_state.get("selected_machine") is not None:
        m = st.session_state.selected_machine
        selected_product_id = str(m.get('Product ID', selected_product_id))
        if m.get('Machine failure') == 1:
            default_issue = f"Critical Failure Repair - Machine {selected_product_id}"
            default_priority_index = 3
        else:
            default_issue = f"Preventive Maintenance - Machine {selected_product_id}"

    next_id = generate_next_wo_id(wo_df)

    with st.form("create_work_order_form", clear_on_submit=True):
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            wo_id = st.text_input("Generated Work Order ID", value=next_id, disabled=True)
            
            prod_id_idx = all_product_ids.index(selected_product_id) if selected_product_id in all_product_ids else 0
            prod_id = st.selectbox("Target Product ID", options=all_product_ids, index=prod_id_idx)
            
            issue = st.text_input("Maintenance Issue / Task Description", value=default_issue)
            
            work_priority = st.selectbox("Priority Level", ["Low", "Medium", "High", "Critical"], index=default_priority_index)

        with col_f2:
            technician = st.selectbox("Assigned Technician", ["Rahul", "Anita", "John", "Priya", "Alex", "David"])
            due_date = st.date_input("Scheduled Due Date", date.today() + timedelta(days=1))
            initial_status = st.selectbox("Initial Status", ["Open", "Assigned", "In Progress"])

        submit_wo = st.form_submit_button("💾 Save & Store Work Order in SQLite")

    if submit_wo:
        add_work_order(next_id, prod_id, issue, work_priority, technician, str(due_date), initial_status)
        st.success(f"✅ Work Order `{next_id}` successfully stored in SQLite database!")
        st.rerun()

    st.markdown("---")

    # 3. WORK ORDER MANAGEMENT (MODULE 6)
    st.subheader("⚙️ Module 6: Search, Filter & Manage Database")

    fc1, fc2, fc3 = st.columns([2, 1, 1])

    with fc1:
        search_query = st.text_input("Search by Work Order ID, Product ID, or Issue Description", "")
    with fc2:
        status_filter = st.selectbox("Filter Status", ["All", "Open", "Assigned", "In Progress", "Completed", "Cancelled"])
    with fc3:
        priority_filter = st.selectbox("Filter Priority", ["All", "Low", "Medium", "High", "Critical"])

    filtered_wo = wo_df.copy()

    if not filtered_wo.empty:
        if search_query:
            filtered_wo = filtered_wo[
                filtered_wo["wo_id"].astype(str).str.contains(search_query, case=False, na=False) |
                filtered_wo["product_id"].astype(str).str.contains(search_query, case=False, na=False) |
                filtered_wo["issue"].astype(str).str.contains(search_query, case=False, na=False)
            ]

        if status_filter != "All":
            filtered_wo = filtered_wo[filtered_wo["status"] == status_filter]

        if priority_filter != "All":
            filtered_wo = filtered_wo[filtered_wo["priority"] == priority_filter]

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(f"📑 Active Records ({len(filtered_wo)})")

    if filtered_wo.empty:
        st.info("No work orders match the selected filters or database is empty.")
    else:
        st.dataframe(filtered_wo, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_u, col_d = st.columns(2)

        with col_u:
            st.markdown("#### 🔄 Update Work Order Status")
            selected_wo_id = st.selectbox("Select Target Work Order ID", options=filtered_wo["wo_id"].unique(), key="update_wo_select")
            new_status = st.selectbox("Select New Status", ["Open", "Assigned", "In Progress", "Completed", "Cancelled"], key="new_status_select")
            
            if st.button("Update Status"):
                update_work_order_status(selected_wo_id, new_status)
                st.success(f"Status for `{selected_wo_id}` updated to **{new_status}**!")
                st.rerun()

        with col_d:
            st.markdown("#### 🗑️ Delete Work Order")
            delete_wo_id = st.selectbox("Select Target Work Order ID to Remove", options=filtered_wo["wo_id"].unique(), key="delete_wo_select")
            
            with st.expander("⚠️ Confirm Deletion"):
                st.warning(f"Are you sure you want to permanently delete record `{delete_wo_id}`?")
                if st.button("🚨 Confirm & Delete"):
                    delete_work_order(delete_wo_id)
                    st.success(f"Work Order `{delete_wo_id}` removed from database!")
                    st.rerun()

        # 4. EXPORT / DOWNLOAD WORK ORDERS SECTION
        st.markdown("---")
        st.subheader("📥 Export Work Orders")
        st.write("Download the current active view or full database directly to your local computer.")

        exp_col1, exp_col2, exp_col3 = st.columns(3)

        # CSV Download Button
        csv_data = filtered_wo.to_csv(index=False).encode('utf-8')
        with exp_col1:
            st.download_button(
                label="📄 Download Records as CSV",
                data=csv_data,
                file_name=f"work_orders_export_{date.today()}.csv",
                mime="text/csv",
                use_container_width=True
            )

        # Excel Download Button
        with exp_col2:
            try:
                excel_data = convert_df_to_excel(filtered_wo)
                st.download_button(
                    label="📊 Download Records as Excel (.xlsx)",
                    data=excel_data,
                    file_name=f"work_orders_export_{date.today()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except Exception:
                pass

        # PDF Download Button
        with exp_col3:
            try:
                pdf_data = convert_df_to_pdf(filtered_wo)
                st.download_button(
                    label="📕 Download Records as PDF",
                    data=pdf_data,
                    file_name=f"work_orders_export_{date.today()}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")