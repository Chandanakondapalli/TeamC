from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor
from datetime import datetime

def generate_workorder_pdf(work_order, filename):
    # -------------------------------------------------
    # Data Sanitization (Prevents crashes from formatting)
    # -------------------------------------------------
    try:
        # Convert cost to float safely, handling commas if they exist
        raw_cost = str(work_order.get('estimated_cost', '0')).replace(',', '')
        formatted_cost = f"${float(raw_cost):,.2f}"
    except (ValueError, TypeError):
        formatted_cost = f"${work_order.get('estimated_cost', '0.00')}"

    doc = SimpleDocTemplate(
        filename,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Define Custom Styles
    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER
    title_style.textColor = HexColor("#0B5394")
    title_style.fontSize = 20

    subtitle_style = styles["Heading2"]
    subtitle_style.alignment = TA_CENTER
    subtitle_style.textColor = HexColor("#333333")
    subtitle_style.fontSize = 14

    heading_style = styles["Heading3"]
    heading_style.textColor = HexColor("#0B5394")
    heading_style.fontSize = 12
    heading_style.spaceAfter = 6

    normal_style = styles["BodyText"]
    normal_style.fontSize = 10
    
    elements = []

    # -------------------------------------------------
    # Header Section
    # -------------------------------------------------
    elements.append(Paragraph("🏭 <b>AGENTIC FACILITYOPS AI PLATFORM</b>", title_style))
    elements.append(Paragraph("<b>MAINTENANCE WORK ORDER REPORT</b>", subtitle_style))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=HexColor("#0B5394")))
    elements.append(Spacer(1, 15))

    # -------------------------------------------------
    # Primary Details Table (ID, Status, Machine)
    # -------------------------------------------------
    details_data = [
        [
            Paragraph(f"<b>Work Order ID :</b> {work_order['work_order_id']}", normal_style),
            Paragraph(f"<b>Status :</b> <font color='#0B5394'><b>{work_order['status'].upper()}</b></font>", normal_style)
        ],
        [
            Paragraph(f"<b>Machine ID :</b> {work_order['machine_id']}", normal_style),
            Paragraph(f"<b>Priority :</b> {work_order['priority']}", normal_style)
        ],
        [
            Paragraph(f"<b>Machine Type :</b> {work_order['machine_type']}", normal_style),
            Paragraph(f"<b>Technician :</b> {work_order['technician']}", normal_style)
        ]
    ]

    details_table = Table(details_data, colWidths=[240, 240])
    details_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    elements.append(details_table)
    elements.append(Spacer(1, 10))

    # -------------------------------------------------
    # Maintenance Info Section
    # -------------------------------------------------
    elements.append(Paragraph("<b>MAINTENANCE LOGISTICS</b>", heading_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=HexColor("#dddddd")))
    elements.append(Spacer(1, 8))

    maint_data = [
        [Paragraph(f"<b>Maintenance Type :</b> {work_order['maintenance_type']}", normal_style),
         Paragraph(f"<b>Estimated Time :</b> {work_order['estimated_time']}", normal_style)],
        [Paragraph(f"<b>Created Date :</b> {work_order['created_date']}", normal_style),
         Paragraph(f"<b>Estimated Cost :</b> {formatted_cost}", normal_style)],
        [Paragraph(f"<b>Due Date :</b> {work_order['due_date']}", normal_style),
         Paragraph("", normal_style)] # Empty cell
    ]

    maint_table = Table(maint_data, colWidths=[240, 240])
    maint_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(maint_table)
    elements.append(Spacer(1, 15))

    # -------------------------------------------------
    # Description Section
    # -------------------------------------------------
    elements.append(Paragraph("<b>WORK DESCRIPTION & INSTRUCTIONS</b>", heading_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=HexColor("#dddddd")))
    elements.append(Spacer(1, 8))

    desc_box_style = styles["BodyText"]
    desc_box_style.leading = 14
    elements.append(Paragraph(work_order.get("description", "No description provided."), desc_box_style))
    elements.append(Spacer(1, 30))

    # -------------------------------------------------
    # Footer Section
    # -------------------------------------------------
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
    elements.append(Spacer(1, 10))
    
    footer_text = f"""
    <b>System Generated Report</b><br/>
    Agentic FacilityOps AI Platform • Internal Use Only<br/>
    Generated On: {datetime.now().strftime('%d-%b-%Y %I:%M %p')}<br/>
    <font color='grey' size='8'>Confidential: This document contains maintenance schedules and operational metadata.</font>
    """

    # FIX: Use normal_style instead of styles["Caption"]
    elements.append(Paragraph(footer_text, normal_style))

    # Build PDF
    doc.build(elements)