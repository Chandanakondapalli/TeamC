import streamlit as st
import ollama

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch

from xml.sax.saxutils import escape


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Maintenance Assistant",
    page_icon="🤖",
    layout="wide"
)


# =====================================================
# TITLE
# =====================================================

st.title(
    "🤖 AI Maintenance Assistant"
)


st.markdown(
    """
    Analyze machine sensor data using **Llama3 AI**
    through the **Ollama runtime** and generate
    intelligent maintenance recommendations.
    """
)


# =====================================================
# CHECK SELECTED MACHINE
# =====================================================

if "selected_machine" not in st.session_state:

    st.warning(
        "⚠️ Please select a machine first from Machine Explorer."
    )

    st.stop()


# =====================================================
# GET SELECTED MACHINE
# =====================================================

machine = st.session_state[
    "selected_machine"
]


# =====================================================
# MACHINE CHANGE DETECTION
# =====================================================

current_machine_id = machine[
    "Product ID"
]


if "ai_machine_id" not in st.session_state:

    st.session_state.ai_machine_id = (
        current_machine_id
    )


elif (

    st.session_state.ai_machine_id
    !=
    current_machine_id

):

    # Clear old chatbot messages

    st.session_state.chat_history = []


    # Clear old AI report

    if "ai_report" in st.session_state:

        del st.session_state[
            "ai_report"
        ]


    # Store new machine

    st.session_state.ai_machine_id = (
        current_machine_id
    )


# =====================================================
# SELECTED MACHINE DETAILS
# =====================================================

st.subheader(
    "🏭 Selected Machine Details"
)


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Product ID",
    machine["Product ID"]
)


col2.metric(
    "Machine ID (UDI)",
    machine["UDI"]
)


col3.metric(
    "Machine Type",
    machine["Type"]
)


if machine["Machine failure"] == 1:

    col4.error(
        "⚠ FAILED"
    )

else:

    col4.success(
        "✅ NORMAL"
    )


st.markdown("---")


# =====================================================
# MACHINE DATA
# =====================================================

machine_data = f"""

Product ID:
{machine['Product ID']}

Machine Type:
{machine['Type']}

Air Temperature:
{machine['Air temperature [K]']} K

Process Temperature:
{machine['Process temperature [K]']} K

Rotational Speed:
{machine['Rotational speed [rpm]']} RPM

Torque:
{machine['Torque [Nm]']} Nm

Tool Wear:
{machine['Tool wear [min]']} minutes

Machine Failure:
{machine['Machine failure']}

Tool Wear Failure:
{machine['TWF']}

Heat Dissipation Failure:
{machine['HDF']}

Power Failure:
{machine['PWF']}

Overstrain Failure:
{machine['OSF']}

Random Failure:
{machine['RNF']}

"""


# =====================================================
# PDF CREATION FUNCTION
# =====================================================

def create_pdf_report(
    machine,
    ai_report
):


    # Create PDF filename

    pdf_file = (
        f"Maintenance_Report_"
        f"{machine['Product ID']}.pdf"
    )


    # Create PDF document

    document = SimpleDocTemplate(

        pdf_file,

        pagesize=A4,

        rightMargin=40,

        leftMargin=40,

        topMargin=40,

        bottomMargin=40

    )


    # Get default styles

    styles = getSampleStyleSheet()


    # Title style

    title_style = ParagraphStyle(

        "CustomTitle",

        parent=styles["Title"],

        alignment=TA_CENTER,

        fontSize=20,

        spaceAfter=20

    )


    # Heading style

    heading_style = ParagraphStyle(

        "CustomHeading",

        parent=styles["Heading2"],

        fontSize=14,

        spaceBefore=15,

        spaceAfter=10

    )


    # Normal text style

    normal_style = ParagraphStyle(

        "CustomNormal",

        parent=styles["BodyText"],

        fontSize=10,

        leading=15,

        spaceAfter=6

    )


    # PDF content

    story = []


    # =================================================
    # REPORT TITLE
    # =================================================

    story.append(

        Paragraph(

            "AI PREDICTIVE MAINTENANCE REPORT",

            title_style

        )

    )


    story.append(
        Spacer(1, 10)
    )


    # =================================================
    # MACHINE INFORMATION
    # =================================================

    story.append(

        Paragraph(

            "MACHINE INFORMATION",

            heading_style

        )

    )


    story.append(

        Paragraph(

            f"<b>Product ID:</b> "
            f"{escape(str(machine['Product ID']))}",

            normal_style

        )

    )


    story.append(

        Paragraph(

            f"<b>Machine ID (UDI):</b> "
            f"{escape(str(machine['UDI']))}",

            normal_style

        )

    )


    story.append(

        Paragraph(

            f"<b>Machine Type:</b> "
            f"{escape(str(machine['Type']))}",

            normal_style

        )

    )


    # =================================================
    # SENSOR VALUES
    # =================================================

    story.append(

        Paragraph(

            "SENSOR VALUES",

            heading_style

        )

    )


    story.append(

        Paragraph(

            f"<b>Air Temperature:</b> "
            f"{machine['Air temperature [K]']} K",

            normal_style

        )

    )


    story.append(

        Paragraph(

            f"<b>Process Temperature:</b> "
            f"{machine['Process temperature [K]']} K",

            normal_style

        )

    )


    story.append(

        Paragraph(

            f"<b>Rotational Speed:</b> "
            f"{machine['Rotational speed [rpm]']} RPM",

            normal_style

        )

    )


    story.append(

        Paragraph(

            f"<b>Torque:</b> "
            f"{machine['Torque [Nm]']} Nm",

            normal_style

        )

    )


    story.append(

        Paragraph(

            f"<b>Tool Wear:</b> "
            f"{machine['Tool wear [min]']} minutes",

            normal_style

        )

    )


    story.append(

        Paragraph(

            f"<b>Machine Failure:</b> "
            f"{machine['Machine failure']}",

            normal_style

        )

    )


    # =================================================
    # AI REPORT
    # =================================================

    story.append(

        Paragraph(

            "AI GENERATED MAINTENANCE ANALYSIS",

            heading_style

        )

    )


    # Add AI report line by line

    for line in ai_report.split("\n"):


        line = line.strip()


        if line:


            # Escape special HTML characters

            safe_line = escape(
                line
            )


            # Make headings bold

            if (

                safe_line.startswith("1.")
                or safe_line.startswith("2.")
                or safe_line.startswith("3.")
                or safe_line.startswith("4.")
                or safe_line.startswith("5.")
                or safe_line.startswith("6.")
                or safe_line.startswith("7.")

            ):


                story.append(

                    Paragraph(

                        f"<b>{safe_line}</b>",

                        normal_style

                    )

                )


            else:


                story.append(

                    Paragraph(

                        safe_line,

                        normal_style

                    )

                )


    # Build PDF

    document.build(
        story
    )


    return pdf_file


# =====================================================
# GENERATE MAINTENANCE REPORT
# =====================================================

st.subheader(
    "📄 AI Maintenance Report"
)


if st.button(

    "🤖 Generate Maintenance Report",

    type="primary",

    width="stretch"

):


    # AI prompt

    prompt = f"""

You are an expert Predictive Maintenance Engineer.

Analyze the following machine data:

{machine_data}

Generate a professional maintenance report.

Include:

1. Overall Machine Health

2. Failure Risk Level

3. Possible Failure Causes

4. Sensor Analysis

5. Recommended Maintenance

6. Preventive Actions

7. Final Conclusion

Keep the report clear, professional,
and easy for a maintenance technician to understand.

"""


    # Run Ollama

    with st.spinner(

        "🤖 AI is analyzing machine data..."

    ):


        response = ollama.chat(

            model="llama3",

            messages=[

                {

                    "role": "user",

                    "content": prompt

                }

            ]

        )


    # Get AI response

    ai_report = response[
        "message"
    ][
        "content"
    ]


    # Store report

    st.session_state[
        "ai_report"
    ] = ai_report


    st.success(
        "✅ Report Generated Successfully!"
    )


# =====================================================
# DISPLAY AI REPORT
# =====================================================

if "ai_report" in st.session_state:


    st.markdown("---")


    st.subheader(
        "📄 Generated Maintenance Report"
    )


    # Display report

    st.markdown(

        st.session_state[
            "ai_report"
        ]

    )


    # =================================================
    # CREATE PDF
    # =================================================

    pdf_file = create_pdf_report(

        machine,

        st.session_state[
            "ai_report"
        ]

    )


    # Read PDF file

    with open(

        pdf_file,

        "rb"

    ) as file:


        pdf_data = file.read()


    # Download button

    st.download_button(

        label="📥 Download Maintenance Report as PDF",

        data=pdf_data,

        file_name=(

            f"Maintenance_Report_"

            f"{machine['Product ID']}.pdf"

        ),

        mime="application/pdf",

        width="stretch"

    )


# =====================================================
# INTERACTIVE AI CHATBOT
# =====================================================

st.markdown("---")


st.subheader(
    "💬 Ask AI About This Machine"
)


st.markdown(

    "Ask questions about the selected machine's "
    "sensor values, health, failures, and maintenance."

)


# =====================================================
# INITIALIZE CHAT HISTORY
# =====================================================

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


# =====================================================
# DISPLAY CHAT HISTORY
# =====================================================

for chat in st.session_state.chat_history:


    with st.chat_message(

        chat["role"]

    ):


        st.write(

            chat["content"]

        )


# =====================================================
# CHAT INPUT
# =====================================================

user_question = st.chat_input(

    "Ask something about this machine..."

)


# =====================================================
# PROCESS QUESTION
# =====================================================

if user_question:


    # Store user question

    st.session_state.chat_history.append(

        {

            "role": "user",

            "content": user_question

        }

    )


    # Chat prompt

    prompt = f"""

You are a predictive maintenance AI assistant.

Machine Information:

{machine_data}

User Question:

{user_question}

Answer clearly and professionally.

Only provide information related to the selected machine.

"""


    # Ask AI

    with st.spinner(

        "🤖 AI is thinking..."

    ):


        response = ollama.chat(

            model="llama3",

            messages=[

                {

                    "role": "user",

                    "content": prompt

                }

            ]

        )


    # Get response

    answer = response[
        "message"
    ][
        "content"
    ]


    # Store AI answer

    st.session_state.chat_history.append(

        {

            "role": "assistant",

            "content": answer

        }

    )


    # Refresh page

    st.rerun()