import datetime
import io
import sqlite3
import subprocess
import sys

required_libraries = ['plotly', 'matplotlib', 'seaborn', 'requests', 'reportlab']
for lib in required_libraries:
    try:
        __import__(lib)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', lib])

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
import requests
import seaborn as sns
import streamlit as st

st.set_page_config(
    page_title='Agentic FacilityOps AI Platform',
    layout='wide',
    initial_sidebar_state='expanded',
)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'user_role' not in st.session_state:
    st.session_state.user_role = None

if 'username' not in st.session_state:
    st.session_state.username = None

st.markdown(
    """
    <style>
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0b0f19 !important;
        color: #f3f4f6 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1f2937 !important;
    }
    [data-testid="stSidebar"] * {
        color: #e5e7eb !important;
    }
    
    p, span, label, h1, h2, h3, h4, h5, h6, .stMarkdown {
        color: #f3f4f6 !important;
    }
    .main-title {
        font-size: 30px;
        font-weight: 800;
        color: #ffffff !important;
        margin-bottom: 2px;
    }
    .sub-title {
        font-size: 15px;
        color: #9ca3af !important;
        margin-top: 0px;
        margin-bottom: 25px;
    }
    .section-header {
        font-size: 18px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 12px;
        color: #ffffff !important;
    }
    
    .stButton>button, .stDownloadButton>button, [data-testid="stFormSubmitButton"]>button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 6px !important;
        font-weight: 800 !important;
        font-size: 14px !important;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button *, .stDownloadButton>button *, [data-testid="stFormSubmitButton"]>button * {
        color: #000000 !important;
        font-weight: 800 !important;
    }
    .stButton>button:hover, .stDownloadButton>button:hover, [data-testid="stFormSubmitButton"]>button:hover {
        background-color: #e2e8f0 !important;
        color: #000000 !important;
        box-shadow: 0 4px 12px rgba(255, 255, 255, 0.2);
    }
    
    div[data-testid="stHorizontalBlock"] .stButton>button {
        background-color: #1f2937 !important;
        color: #000000 !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
        padding: 10px 16px !important;
        font-weight: 800 !important;
        font-size: 13px !important;
        width: 100% !important;
    }
    div[data-testid="stHorizontalBlock"] .stButton>button:hover {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-color: #ffffff !important;
    }
    
    div[data-testid="stMetric"] {
        background-color: #1f2937 !important;
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    div[data-testid="stMetricLabel"] {
        color: #9ca3af !important;
        font-weight: 700 !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 800 !important;
    }
    
    .wo-card {
        background-color: #1f2937 !important;
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 18px 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .wo-card-blue { border-top: 4px solid #3b82f6 !important; }
    .wo-card-green { border-top: 4px solid #10b981 !important; }
    .wo-card-orange { border-top: 4px solid #f59e0b !important; }
    .wo-card-red { border-top: 4px solid #ef4444 !important; }
    .wo-card-purple { border-top: 4px solid #8b5cf6 !important; }
    
    .wo-card-title {
        font-size: 11px;
        font-weight: 700;
        color: #9ca3af !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    .wo-card-value {
        font-size: 28px;
        font-weight: 800;
        color: #ffffff !important;
        line-height: 1;
    }
    .wo-card-sub {
        font-size: 11px;
        color: #9ca3af !important;
        margin-top: 6px;
    }
    
    .health-card-critical {
        background-color: #2a1215 !important;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 6px solid #ef4444 !important;
        border: 1px solid #451a1d;
    }
    .health-card-good {
        background-color: #062319 !important;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 6px solid #10b981 !important;
        border: 1px solid #0b3c26;
    }
    .card-label {
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        color: #9ca3af !important;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .health-title-critical {
        font-size: 26px;
        font-weight: 800;
        color: #fca5a5 !important;
        margin-bottom: 4px;
    }
    .health-title-good {
        font-size: 26px;
        font-weight: 800;
        color: #6ee7b7 !important;
        margin-bottom: 4px;
    }
    .health-subtitle {
        font-size: 14px;
        color: #f3f4f6 !important;
    }
    
    .badge-pass {
        color: #6ee7b7 !important;
        background-color: #064e3b !important;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 12px;
        margin-right: 8px;
    }
    .badge-fail {
        color: #fca5a5 !important;
        background-color: #7f1d1d !important;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 12px;
        margin-right: 8px;
    }
    
    .detail-sheet-box {
        background-color: #1f2937 !important;
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    
    .stTextInput input, .stSelectbox select, .stTextArea textarea, .stNumberInput input {
        background-color: #111827 !important;
        color: #ffffff !important;
        border: 1px solid #374151 !important;
        border-radius: 6px !important;
    }
    .stMultiSelect div[role="button"] {
        background-color: #1f2937 !important;
        color: #ffffff !important;
    }
    
    .relationship-box {
        background-color: #1f2937 !important;
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 24px;
        margin-top: 20px;
    }
    .relationship-title {
        color: #ffffff !important;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 2px;
    }
    .relationship-subtitle {
        color: #9ca3af !important;
        font-size: 13px;
        margin-bottom: 25px;
    }
    .chart-label {
        color: #ffffff !important;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 12px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

def render_login_screen():
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        st.markdown('<br><br>', unsafe_allow_html=True)
        st.markdown(
            """
            <div style='text-align: center; margin-bottom: 20px;'>
                <h1 style='font-weight: 800; color: #ffffff; margin-bottom: 0px;'>Agentic FacilityOps</h1>
                <p style='color: #3b82f6; font-size: 14px; letter-spacing: 1px; font-weight: 700;'>INDUSTRIAL ANALYTICS PLATFORM</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form('login_form'):
            st.markdown('### 🔒 System Authentication')
            username_inp = st.text_input('Username or Employee ID', placeholder='admin')
            password_inp = st.text_input(
                'Password', type='password', placeholder='••••••••'
            )
            role_inp = st.selectbox(
                'Operational Role',
                ['Shop Floor Lead', 'Maintenance Engineer', 'Facility Ops Admin'],
            )

            st.markdown('<br>', unsafe_allow_html=True)
            submit_login = st.form_submit_button(
                '🔑 Login to Platform', use_container_width=True
            )

            if submit_login:
                if (username_inp == 'admin' and password_inp == 'admin') or (
                    username_inp != '' and password_inp != ''
                ):
                    st.session_state.authenticated = True
                    st.session_state.username = (
                        username_inp if username_inp else 'Admin User'
                    )
                    st.session_state.user_role = role_inp
                    st.toast('✅ Authenticated Successfully!', icon='🎉')
                    st.rerun()
                else:
                    st.error('❌ Invalid Username or Password. Please try again.')

if not st.session_state.authenticated:
    render_login_screen()
    st.stop()

DB_NAME = 'facilityops.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS work_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id TEXT NOT NULL,
            issue_type TEXT NOT NULL,
            priority TEXT NOT NULL,
            technician TEXT NOT NULL,
            created_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            status TEXT NOT NULL,
            description TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS pm_schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id TEXT NOT NULL,
            task_name TEXT NOT NULL,
            frequency TEXT NOT NULL,
            technician TEXT NOT NULL,
            last_performed TEXT NOT NULL,
            next_due TEXT NOT NULL,
            status TEXT NOT NULL,
            checklist TEXT,
            completion_history TEXT
        )
    ''')
    conn.commit()

    c.execute('SELECT COUNT(*) FROM pm_schedules')
    if c.fetchone()[0] == 0:
        sample_schedules = [
            (
                'M14860',
                'Spindle Bearing Lubrication',
                'Monthly',
                'Alex',
                '2026-07-01',
                '2026-08-01',
                'Overdue',
                (
                    'Inspect oil seals; Apply ISO VG 68 lubricant; Check vibration'
                    ' levels.'
                ),
            ),
            (
                'L47249',
                'Coolant Thermal Calibration',
                'Weekly',
                'Sarah',
                '2026-07-28',
                '2026-08-04',
                'Due Today',
                (
                    'Check coolant flow rate; Clean radiator fins; Calibrate temp'
                    ' sensor.'
                ),
            ),
            (
                'H29424',
                'Drive Belt Tension & Wear Check',
                'Bi-Weekly',
                'John',
                '2026-07-20',
                '2026-08-10',
                'Scheduled',
                (
                    'Inspect belt teeth; Measure tension gauge; Tighten drive'
                    ' assembly.'
                ),
            ),
            (
                'M24000',
                'Electrical Panel Lockout/Tagout Inspection',
                'Quarterly',
                'David',
                '2026-05-15',
                '2026-08-15',
                'Scheduled',
                (
                    'Inspect breaker contacts; Test grounding bus; Thermal scan'
                    ' terminal block.'
                ),
            ),
        ]
        c.executemany(
            '''
            INSERT INTO pm_schedules (asset_id, task_name, frequency, technician, last_performed, next_due, status, checklist)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            sample_schedules,
        )
        conn.commit()

    conn.close()

init_db()

def get_work_orders_df():
    conn = sqlite3.connect(DB_NAME)
    df_wo = pd.read_sql_query('SELECT * FROM work_orders ORDER BY id DESC', conn)
    conn.close()
    return df_wo

def add_work_order(
    asset_id,
    issue_type,
    priority,
    technician,
    due_date,
    status,
    description='',
):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    created_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute(
        '''
        INSERT INTO work_orders (asset_id, issue_type, priority, technician, created_date, due_date, status, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (
            asset_id,
            issue_type,
            priority,
            technician,
            created_date,
            str(due_date),
            status,
            description,
        ),
    )
    conn.commit()
    conn.close()

def update_work_order(wo_id, priority, technician, due_date, status, description):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        '''
        UPDATE work_orders
        SET priority = ?, technician = ?, due_date = ?, status = ?, description = ?
        WHERE id = ?
        ''',
        (priority, technician, str(due_date), status, description, wo_id),
    )
    conn.commit()
    conn.close()

def delete_work_order(wo_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM work_orders WHERE id = ?', (wo_id,))
    conn.commit()
    conn.close()

def get_pm_schedules_df():
    conn = sqlite3.connect(DB_NAME)
    df_pm = pd.read_sql_query(
        'SELECT * FROM pm_schedules ORDER BY next_due ASC', conn
    )
    conn.close()
    return df_pm

def add_pm_schedule(
    asset_id,
    task_name,
    frequency,
    technician,
    last_performed,
    next_due,
    status,
    checklist,
):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        '''
        INSERT INTO pm_schedules (asset_id, task_name, frequency, technician, last_performed, next_due, status, checklist)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (
            asset_id,
            task_name,
            frequency,
            technician,
            str(last_performed),
            str(next_due),
            status,
            checklist,
        ),
    )
    conn.commit()
    conn.close()

def update_pm_status(pm_id, status, last_performed, next_due):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        '''
        UPDATE pm_schedules
        SET status = ?, last_performed = ?, next_due = ?
        WHERE id = ?
        ''',
        (status, str(last_performed), str(next_due), pm_id),
    )
    conn.commit()
    conn.close()

def generate_work_order_pdf(wo_row, machine_info=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    story = []

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=2,
    )

    sub_title_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor('#475569'),
        spaceAfter=15,
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=12,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#334155'),
    )

    wo_id = wo_row['id']
    issued_date = wo_row['created_date']
    story.append(
        Paragraph(f'<b>MAINTENANCE WORK ORDER — #{wo_id}</b>', title_style)
    )
    story.append(
        Paragraph(f'<b>Issued Date & Time:</b> {issued_date}', sub_title_style)
    )
    story.append(Spacer(1, 5))

    m_type = (
        machine_info['Type'] if machine_info is not None else 'High Quality (H)'
    )
    m_udi = machine_info['UDI'] if machine_info is not None else '11'

    type_full = (
        f'High Quality ({m_type})'
        if m_type == 'H'
        else (
            f'Medium Quality ({m_type})'
            if m_type == 'M'
            else f'Low Quality ({m_type})'
        )
    )
    status_str = (
        'OPTIMAL (100.0%)'
        if wo_row['status'] == 'Completed'
        else f"{wo_row['status'].upper()} (ATTENTION REQUIRED)"
    )

    story.append(Paragraph('<b>Work Order Telemetry Sheet</b>', section_heading))

    table_data = [
        [
            Paragraph('<b>Work Order ID</b>', body_style),
            Paragraph(str(wo_id), body_style),
        ],
        [
            Paragraph('<b>Product ID</b>', body_style),
            Paragraph(str(wo_row['asset_id']), body_style),
        ],
        [
            Paragraph('<b>Machine ID</b>', body_style),
            Paragraph(str(m_udi), body_style),
        ],
        [
            Paragraph('<b>Machine Type</b>', body_style),
            Paragraph(type_full, body_style),
        ],
        [
            Paragraph('<b>Machine Quality Class</b>', body_style),
            Paragraph(str(m_type), body_style),
        ],
        [
            Paragraph('<b>Current Machine Status</b>', body_style),
            Paragraph(status_str, body_style),
        ],
        [
            Paragraph('<b>Failure Type (If available)</b>', body_style),
            Paragraph(str(wo_row['issue_type']), body_style),
        ],
        [
            Paragraph('<b>Priority</b>', body_style),
            Paragraph(str(wo_row['priority']), body_style),
        ],
        [
            Paragraph('<b>Date & Time</b>', body_style),
            Paragraph(str(wo_row['created_date']), body_style),
        ],
    ]

    t = Table(table_data, colWidths=[200, 340])
    t.setStyle(
        TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
    )
    story.append(t)
    story.append(Spacer(1, 15))

    story.append(Paragraph('<b>Job Description</b>', section_heading))
    desc_text = (
        wo_row['description']
        if wo_row['description']
        else 'No additional description provided.'
    )
    story.append(Paragraph(desc_text, body_style))
    story.append(Spacer(1, 15))

    story.append(Paragraph('<b>Recommended Maintenance</b>', section_heading))
    rec_text = (
        'Standard preventative inspection: Calibrate speed encoders, clean'
        ' spindle housing, and check thermal couplings.'
    )
    story.append(Paragraph(rec_text, body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

@st.cache_data
def load_data():
    file_path = 'data/ai4i2020.csv'
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        try:
            df = pd.read_csv('ai4i2020.csv')
        except FileNotFoundError:
            try:
                df = pd.read_csv('predictive_maintenance.csv')
            except FileNotFoundError:
                st.error(f"❌ File '{file_path}' not found in project directory!")
                st.stop()

    df.columns = [c.strip() for c in df.columns]

    rename_map = {
        'UID': 'UDI',
        'Air temperature': 'Air temperature [K]',
        'Process temperature': 'Process temperature [K]',
        'Rotational speed': 'Rotational speed [rpm]',
        'Torque': 'Torque [Nm]',
        'Tool wear': 'Tool wear [min]',
    }
    df = df.rename(columns=rename_map)

    cols_to_numeric = [
        'Air temperature [K]',
        'Process temperature [K]',
        'Rotational speed [rpm]',
        'Torque [Nm]',
        'Tool wear [min]',
        'Machine failure',
        'TWF',
        'HDF',
        'PWF',
        'OSF',
        'RNF',
    ]
    for col in cols_to_numeric:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    failure_cols = [
        c for c in ['TWF', 'HDF', 'PWF', 'OSF', 'RNF'] if c in df.columns
    ]
    if failure_cols:
        failure_mask = df[failure_cols].sum(axis=1) > 0
        df.loc[failure_mask, 'Machine failure'] = 1

    return df

df = load_data()
df['Status Mapping'] = (
    df['Machine failure'].map({0: 'Healthy', 1: 'Failed'}).fillna('Healthy')
)

st.sidebar.markdown(
    "<h2 style='font-size:20px; font-weight:800; color:#ffffff;'>Agentic FacilityOps</h2>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "<p style='color:#3b82f6; font-size:11px; margin-top:-15px; margin-bottom:15px; font-weight:700;'>INDUSTRIAL ANALYTICS PLATFORM</p>",
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    f"""
    <div style="background-color: #1f2937; border: 1px solid #374151; border-radius: 6px; padding: 12px; margin-bottom: 15px;">
        <span style="font-size: 10px; font-weight: 800; color: #9ca3af; letter-spacing: 0.5px;">ACTIVE SESSION</span><br>
        <span style="font-size: 14px; font-weight: 800; color: #ffffff;">👤 {st.session_state.username}</span><br>
        <span style="font-size: 11px; color: #d1d5db;">Role: {st.session_state.user_role}</span>
    </div>
""",
    unsafe_allow_html=True,
)

if st.sidebar.button('🚪 Logout', use_container_width=True):
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_role = None
    st.rerun()

st.sidebar.markdown(
    "<br><h3 style='margin-bottom:0px; font-size:14px; color:#ffffff;'>🔍 Filters</h3>", unsafe_allow_html=True
)

all_types = list(df['Type'].unique())
selected_types = st.sidebar.multiselect(
    'Select Machine Type', options=all_types, default=all_types
)

status_options = ['All', 'Healthy', 'Failed']
selected_status = st.sidebar.selectbox(
    'Machine Status', options=status_options, index=0
)

filtered_df = df[df['Type'].isin(selected_types)].copy()
if selected_status == 'Healthy':
    filtered_df = filtered_df[filtered_df['Machine failure'] == 0]
elif selected_status == 'Failed':
    filtered_df = filtered_df[filtered_df['Machine failure'] == 1]

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Executive Dashboard'

nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns(6)

with nav_col1:
    if st.button('📊 Dashboard', use_container_width=True):
        st.session_state.current_page = 'Executive Dashboard'
        st.rerun()

with nav_col2:
    if st.button('📈 EDA', use_container_width=True):
        st.session_state.current_page = 'Module 1: EDA'
        st.rerun()

with nav_col3:
    if st.button('🏭 Explorer', use_container_width=True):
        st.session_state.current_page = 'Machine Explorer'
        st.rerun()

with nav_col4:
    if st.button('🤖 AI Assistant', use_container_width=True):
        st.session_state.current_page = 'AI Maintenance Assistant'
        st.rerun()

with nav_col5:
    if st.button('🛠️ Work Orders', use_container_width=True):
        st.session_state.current_page = 'Work Order Console'
        st.rerun()

with nav_col6:
    if st.button('📅 Preventive PM', use_container_width=True):
        st.session_state.current_page = 'Module 7: Preventive Maintenance'
        st.rerun()

app_mode = st.session_state.current_page
st.markdown("<hr style='border-color: #374151; margin-top: 5px; margin-bottom: 20px;'>", unsafe_allow_html=True)

if app_mode == 'Executive Dashboard':
    st.markdown(
        '<p class="main-title">🏭 Industrial Analytics Dashboard</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="sub-title">Predictive Maintenance Dashboard</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="section-header">Dataset Overview & Data Types</p>',
        unsafe_allow_html=True,
    )

    r1_1, r1_2, r1_3, r1_4 = st.columns(4)
    with r1_1:
        st.markdown(
            f'''
            <div class="wo-card wo-card-blue">
                <div class="wo-card-title">TOTAL ROWS</div>
                <div class="wo-card-value">{len(filtered_df):,}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
    with r1_2:
        st.markdown(
            f'''
            <div class="wo-card wo-card-blue">
                <div class="wo-card-title">TOTAL COLUMNS</div>
                <div class="wo-card-value">{len(filtered_df.columns)}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
    with r1_3:
        st.markdown(
            f'''
            <div class="wo-card wo-card-green">
                <div class="wo-card-title">MISSING VALUES</div>
                <div class="wo-card-value">{filtered_df.isnull().sum().sum()}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
    with r1_4:
        st.markdown(
            f'''
            <div class="wo-card wo-card-green">
                <div class="wo-card-title">DUPLICATE VALUES</div>
                <div class="wo-card-value">{filtered_df.duplicated().sum()}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

    r2_1, r2_2, r2_3, r2_4 = st.columns(4)
    num_cols = filtered_df.select_dtypes(include=[np.number]).columns
    cat_cols = filtered_df.select_dtypes(exclude=[np.number]).columns
    int_cols = filtered_df.select_dtypes(include=['int64', 'int32']).columns
    float_cols = filtered_df.select_dtypes(include=['float64', 'float32']).columns

    with r2_1:
        st.markdown(
            f'''
            <div class="wo-card wo-card-purple">
                <div class="wo-card-title">NUMERICAL COLUMNS</div>
                <div class="wo-card-value">{len(num_cols)}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
    with r2_2:
        st.markdown(
            f'''
            <div class="wo-card wo-card-purple">
                <div class="wo-card-title">CATEGORICAL COLUMNS</div>
                <div class="wo-card-value">{len(cat_cols)}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
    with r2_3:
        st.markdown(
            f'''
            <div class="wo-card wo-card-purple">
                <div class="wo-card-title">INTEGER COLUMNS</div>
                <div class="wo-card-value">{len(int_cols)}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
    with r2_4:
        st.markdown(
            f'''
            <div class="wo-card wo-card-purple">
                <div class="wo-card-title">FLOAT COLUMNS</div>
                <div class="wo-card-value">{len(float_cols)}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<p class="section-header">📌 Operational Overview Metrics</p>',
        unsafe_allow_html=True,
    )
    avg_rpm = filtered_df['Rotational speed [rpm]'].mean() if len(filtered_df) > 0 else 0
    avg_torque = filtered_df['Torque [Nm]'].mean() if len(filtered_df) > 0 else 0
    avg_temp = filtered_df['Air temperature [K]'].mean() if len(filtered_df) > 0 else 0
    avg_wear = filtered_df['Tool wear [min]'].mean() if len(filtered_df) > 0 else 0

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(
            f'''
            <div class="wo-card wo-card-blue">
                <div class="wo-card-title">AVERAGE TOOL WEAR</div>
                <div class="wo-card-value">{avg_wear:.1f} min</div>
                <div class="wo-card-sub">0 min — 253 min Max</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            f'''
            <div class="wo-card wo-card-green">
                <div class="wo-card-title">AVG ROTATIONAL SPEED</div>
                <div class="wo-card-value">{int(avg_rpm)} RPM</div>
                <div class="wo-card-sub">0 RPM — 2886 Max</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            f'''
            <div class="wo-card wo-card-orange">
                <div class="wo-card-title">AVG TORQUE</div>
                <div class="wo-card-value">{avg_torque:.1f} Nm</div>
                <div class="wo-card-sub">0 Nm — 76.6 Max</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
    with k4:
        st.markdown(
            f'''
            <div class="wo-card wo-card-red">
                <div class="wo-card-title">AVG AIR TEMPERATURE</div>
                <div class="wo-card-value">{avg_temp:.1f} K</div>
                <div class="wo-card-sub">295.3 K Min — 304.5 Max</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

    st.markdown('<br>', unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.markdown(
            '<div class="wo-card"><p class="chart-label">Failure Distribution</p>',
            unsafe_allow_html=True,
        )
        fail_summary = filtered_df['Status Mapping'].value_counts().reset_index()
        fail_summary.columns = ['Status Mapping', 'count']
        fig_donut = px.pie(
            fail_summary,
            values='count',
            names='Status Mapping',
            hole=0.6,
            color='Status Mapping',
            color_discrete_map={'Healthy': '#10b981', 'Failed': '#ef4444'},
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent')
        fig_donut.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            height=320,
            margin=dict(l=20, r=20, t=10, b=20),
            legend=dict(font=dict(color='#ffffff')),
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with chart_col2:
        st.markdown(
            '<div class="wo-card"><p class="chart-label">Tool Wear by Failure State</p>',
            unsafe_allow_html=True,
        )
        fig_box = px.box(
            filtered_df,
            x='Status Mapping',
            y='Tool wear [min]',
            color='Status Mapping',
            color_discrete_map={'Healthy': '#10b981', 'Failed': '#ef4444'},
        )
        fig_box.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            height=320,
            margin=dict(l=40, r=20, t=10, b=40),
            xaxis=dict(
                title=dict(
                    text='Machine Failure Status',
                    font=dict(color='#9ca3af', size=12),
                ),
                tickfont=dict(color='#ffffff'),
                gridcolor='#374151',
            ),
            yaxis=dict(
                title=dict(
                    text='Tool Wear (min)', font=dict(color='#9ca3af', size=12)
                ),
                tickfont=dict(color='#ffffff'),
                gridcolor='#374151',
            ),
            showlegend=False,
        )
        st.plotly_chart(fig_box, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif app_mode == 'Module 1: EDA':
    st.markdown(
        '<p class="main-title">📊 Exploratory Data Analysis (EDA)</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="sub-title">Overview & Quality • Statistical Analysis • Distribution</p>',
        unsafe_allow_html=True,
    )

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.subheader('Missing Value Profile')
        st.dataframe(
            filtered_df.isnull().sum().to_frame('Missing Count'),
            use_container_width=True,
        )
    with col_e2:
        st.subheader('Descriptive Summary Statistics')
        st.dataframe(filtered_df.describe(), use_container_width=True)

    st.markdown('---')
    col_e3, col_e4 = st.columns(2)
    with col_e3:
        st.subheader('Feature Distributions')
        hist_var = st.selectbox(
            'Pick column for Histogram',
            [
                'Air temperature [K]',
                'Process temperature [K]',
                'Rotational speed [rpm]',
                'Torque [Nm]',
                'Tool wear [min]',
            ],
        )
        fig_hist = px.histogram(
            filtered_df, x=hist_var, color='Status Mapping', barmode='overlay'
        )
        fig_hist.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            xaxis=dict(gridcolor='#374151'),
            yaxis=dict(gridcolor='#374151'),
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_e4:
        st.subheader('Correlation Matrix')
        matrix_cols = [
            'UDI',
            'Air temperature [K]',
            'Process temperature [K]',
            'Rotational speed [rpm]',
            'Torque [Nm]',
            'Tool wear [min]',
            'Machine failure',
            'TWF',
            'HDF',
            'PWF',
            'OSF',
            'RNF',
        ]
        available_cols = [col for col in matrix_cols if col in filtered_df.columns]
        corr_matrix = filtered_df[available_cols].corr().fillna(0)

        fig_heat, ax = plt.subplots(figsize=(10, 8), facecolor='none')
        ax.set_facecolor('none')
        sns.heatmap(
            corr_matrix,
            annot=True,
            cmap='coolwarm',
            fmt='.2g',
            annot_kws={'size': 8, 'color': 'white'},
            ax=ax,
            cbar=True,
            vmin=-1,
            vmax=1,
        )
        plt.xticks(rotation=90, color='white')
        plt.yticks(rotation=0, color='white')
        plt.tight_layout()
        st.pyplot(fig_heat)

    st.markdown('---')
    st.subheader('📌 Correlation Insights Summary')
    
    st.markdown(
        '<p class="relationship-subtitle">These visualizations highlight relationships between important machine parameters and machine failure.</p>',
        unsafe_allow_html=True,
    )

    scat_col1, scat_col2 = st.columns(2)

    with scat_col1:
        st.markdown(
            '<p class="chart-label">Relationship Between Rotational Speed and Torque</p>',
            unsafe_allow_html=True,
        )
        fig_scat1 = px.scatter(
            filtered_df,
            x='Rotational speed [rpm]',
            y='Torque [Nm]',
            color=filtered_df['Machine failure'].astype(int).astype(str),
            color_discrete_map={'0': '#E11D48', '1': '#2563EB'},
        )
        fig_scat1.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='rgba(0,0,0,0)',
            height=380,
            margin=dict(l=50, r=20, t=10, b=50),
            legend=dict(title_text='Failure', font=dict(color='white')),
            xaxis=dict(
                title=dict(
                    text='Rotational Speed (RPM)',
                    font=dict(color='#ffffff', size=12),
                ),
                tickfont=dict(color='#ffffff', size=10),
                gridcolor='#374151',
                showline=True,
                linecolor='#CBD5E1',
            ),
            yaxis=dict(
                title=dict(
                    text='Torque (Nm)', font=dict(color='#ffffff', size=12)
                ),
                tickfont=dict(color='#ffffff', size=10),
                gridcolor='#374151',
                showline=True,
                linecolor='#CBD5E1',
            ),
        )
        st.plotly_chart(fig_scat1, use_container_width=True)

    with scat_col2:
        st.markdown(
            '<p class="chart-label">Relationship Between Air and Process Temperature</p>',
            unsafe_allow_html=True,
        )
        fig_scat2 = px.scatter(
            filtered_df,
            x='Air temperature [K]',
            y='Process temperature [K]',
            color=filtered_df['Machine failure'].astype(int).astype(str),
            color_discrete_map={'0': '#10B981', '1': '#F97316'},
        )
        fig_scat2.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='rgba(0,0,0,0)',
            height=380,
            margin=dict(l=50, r=20, t=10, b=50),
            legend=dict(title_text='Failure', font=dict(color='white')),
            xaxis=dict(
                title=dict(
                    text='Air Temperature (K)', font=dict(color='#ffffff', size=12)
                ),
                tickfont=dict(color='#ffffff', size=10),
                gridcolor='#374151',
                showline=True,
                linecolor='#CBD5E1',
            ),
            yaxis=dict(
                title=dict(
                    text='Process Temperature (K)',
                    font=dict(color='#ffffff', size=12),
                ),
                tickfont=dict(color='#ffffff', size=10),
                gridcolor='#374151',
                showline=True,
                linecolor='#CBD5E1',
            ),
        )
        st.plotly_chart(fig_scat2, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif app_mode == 'Machine Explorer':
    st.markdown(
        '<h2 style="margin-bottom:0px; color:#ffffff;">🏭 Machine Explorer</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#9ca3af;font-size:14px;">Search and analyze an industrial machine</p>',
        unsafe_allow_html=True,
    )
    st.markdown('<br>', unsafe_allow_html=True)

    st.markdown('### 📄 Machine Data')
    st.dataframe(
        filtered_df[[
            'UDI',
            'Product ID',
            'Type',
            'Air temperature [K]',
            'Process temperature [K]',
            'Rotational speed [rpm]',
            'Torque [Nm]',
            'Tool wear [min]',
            'Machine failure',
            'TWF',
            'HDF',
            'PWF',
            'OSF',
            'RNF',
        ]],
        use_container_width=True,
        height=200,
    )

    st.markdown('<br>', unsafe_allow_html=True)
    search_pid = st.selectbox(
        'Select or Search Product ID:', df['Product ID'].unique()
    )
    selected_row = df[df['Product ID'] == search_pid]

    if len(selected_row) > 0:
        m = selected_row.iloc[0]

        failure_causes = []
        if m.get('TWF', 0) == 1:
            failure_causes.append('Tool Wear')
        if m.get('HDF', 0) == 1:
            failure_causes.append('Heat Dissipation')
        if m.get('PWF', 0) == 1:
            failure_causes.append('Power')
        if m.get('OSF', 0) == 1:
            failure_causes.append('Overstrain')
        if m.get('RNF', 0) == 1:
            failure_causes.append('Random')

        failure_str = ', '.join(failure_causes) if failure_causes else 'None'
        is_failed = (m['Machine failure'] == 1) or (len(failure_causes) > 0)

        main_issue = (
            failure_causes[0] + ' Failure'
            if failure_causes
            else ('General Anomaly' if is_failed else 'General Maintenance')
        )

        if is_failed:
            st.markdown(
                f"""
                <div class="health-card-critical">
                    <div class="card-label">MACHINE HEALTH STATUS</div>
                    <div class="health-title-critical">Critical · 0/100</div>
                    <div class="health-subtitle"><b>{m['Product ID']}</b> · Type {m['Type']} · UDI {m['UDI']} — <b>Recorded failure event:</b> {failure_str}</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="health-card-good">
                    <div class="card-label">MACHINE HEALTH STATUS</div>
                    <div class="health-title-good">Optimal · 100/100</div>
                    <div class="health-subtitle"><b>{m['Product ID']}</b> · Type {m['Type']} · UDI {m['UDI']} — Machine is operating within normal boundaries.</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        if is_failed:
            db_orders = get_work_orders_df()
            existing = db_orders[
                (db_orders['asset_id'] == m['Product ID'])
                & (db_orders['status'].isin(['Open', 'In Progress']))
            ]
            if existing.empty:
                default_due = (
                    datetime.date.today() + datetime.timedelta(days=2)
                ).strftime('%Y-%m-%d')
                add_work_order(
                    asset_id=m['Product ID'],
                    issue_type=main_issue,
                    priority='Critical' if m.get('OSF', 0) == 1 else 'High',
                    technician='Sarah',
                    due_date=default_due,
                    status='Open',
                    description=(
                        'Auto-generated Work Order via AI Machine Explorer for'
                        f' recorded failure event: {failure_str}'
                    ),
                )
                st.toast(
                    '⚡ Faulty machine detected! Work Order automatically logged to'
                    f" SQLite database for Asset ID: {m['Product ID']}",
                    icon='🚨',
                )

        st.markdown(
            '<div class="card-label" style="font-size: 11px; font-weight: bold; letter-spacing: 1px; color: #9ca3af; text-transform: uppercase; margin-bottom: 8px; margin-top: 15px;">RECORDED SENSOR VALUES</div>',
            unsafe_allow_html=True,
        )

        g1, g2, g3, g4, g5 = st.columns(5)

        def create_arc_gauge(value, title, unit, min_v, max_v, bar_color):
            fig = go.Figure(
                go.Indicator(
                    mode='gauge+number',
                    value=value,
                    number={
                        'suffix': f' {unit}',
                        'font': {'size': 18, 'color': '#ffffff', 'family': 'sans-serif'},
                    },
                    gauge={
                        'shape': 'angular',
                        'axis': {'range': [min_v, max_v], 'visible': False},
                        'bar': {'color': bar_color, 'thickness': 0.35},
                        'bgcolor': '#374151',
                        'borderwidth': 0,
                    },
                )
            )
            fig.update_layout(
                height=130,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=25, b=0),
                annotations=[{
                    'text': f'<b>{title}</b>',
                    'x': 0.5,
                    'y': 1.15,
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 12, 'color': '#9ca3af'},
                }],
            )
            return fig

        with g1:
            st.plotly_chart(
                create_arc_gauge(
                    m['Air temperature [K]'],
                    'Air temperature',
                    'K',
                    280,
                    320,
                    '#3b82f6',
                ),
                use_container_width=True,
            )
        with g2:
            st.plotly_chart(
                create_arc_gauge(
                    m['Process temperature [K]'],
                    'Process temperature',
                    'K',
                    290,
                    330,
                    '#f59e0b',
                ),
                use_container_width=True,
            )
        with g3:
            st.plotly_chart(
                create_arc_gauge(
                    m['Rotational speed [rpm]'],
                    'Rotational speed',
                    'rpm',
                    1000,
                    3000,
                    '#10b981',
                ),
                use_container_width=True,
            )
        with g4:
            st.plotly_chart(
                create_arc_gauge(
                    m['Torque [Nm]'], 'Torque', 'Nm', 0, 100, '#ec4899'
                ),
                use_container_width=True,
            )
        with g5:
            st.plotly_chart(
                create_arc_gauge(
                    m['Tool wear [min]'], 'Tool wear', 'min', 0, 250, '#8b5cf6'
                ),
                use_container_width=True,
            )

        st.markdown(
            '<p style="color:#9ca3af; font-size:12px; margin-top:-5px; margin-bottom:'
            ' 20px;">Recorded values from the selected row — not a live sensor'
            ' feed.</p>',
            unsafe_allow_html=True,
        )

        twf_status = (
            '✓ TWF · Tool wear'
            if m.get('TWF', 0) == 0
            else '✖ TWF · Tool wear'
        )
        hdf_status = (
            '✓ HDF · Heat dissipation'
            if m.get('HDF', 0) == 0
            else '✖ HDF · Heat dissipation'
        )
        pwf_status = (
            '✓ PWF · Power' if m.get('PWF', 0) == 0 else '✖ PWF · Power'
        )
        osf_status = (
            '✓ OSF · Overstrain'
            if m.get('OSF', 0) == 0
            else '✖ OSF · Overstrain'
        )
        rnf_status = (
            '✓ RNF · Random' if m.get('RNF', 0) == 0 else '✖ RNF · Random'
        )

        st.markdown(
            f"""
            <div style="background-color: #1f2937; border: 1px solid #374151; border-radius: 8px; padding: 16px; margin-top: 10px; margin-bottom: 20px;">
                <div class="card-label" style="font-size: 11px; font-weight: bold; letter-spacing: 1px; color: #9ca3af; text-transform: uppercase; margin-bottom: 8px;">FAILURE ANALYSIS</div>
                <div style="margin-top: 8px; margin-bottom: 12px;">
                    <span class="{ 'badge-pass' if m.get('TWF',0)==0 else 'badge-fail' }">{twf_status}</span>
                    <span class="{ 'badge-pass' if m.get('HDF',0)==0 else 'badge-fail' }">{hdf_status}</span>
                    <span class="{ 'badge-pass' if m.get('PWF',0)==0 else 'badge-fail' }">{pwf_status}</span>
                    <span class="{ 'badge-pass' if m.get('OSF',0)==0 else 'badge-fail' }">{osf_status}</span>
                    <span class="{ 'badge-pass' if m.get('RNF',0)==0 else 'badge-fail' }">{rnf_status}</span>
                </div>
                <p style="color:#d1d5db; font-size:13px; margin-bottom:0px;"><b>Recorded failure cause:</b> {failure_str}</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown('#### ACTIVE MAINTENANCE WORK ORDERS')
        m_orders = get_work_orders_df()
        m_orders = m_orders[m_orders['asset_id'] == m['Product ID']]

        if not m_orders.empty:
            for _, wo_row in m_orders.iterrows():
                st.markdown(
                    f"""
                    <div style="background-color: #2a1215; border: 1px solid #451a1d; border-radius: 6px; padding: 12px; margin-bottom: 10px;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-weight:bold; color:#fca5a5;">Order #{wo_row['id']} - {wo_row['issue_type']}</span>
                            <span style="background-color:#7f1d1d; color:#fca5a5; font-size:11px; font-weight:bold; padding:2px 8px; border-radius:4px;">{wo_row['status'].upper()}</span>
                        </div>
                        <div style="font-size:12px; color:#fca5a5; margin-top:4px;">
                            Assignee: {wo_row['technician']} | Deadline: {wo_row['due_date']}
                        </div>
                        <div style="font-size:12px; color:#d1d5db; margin-top:4px;">
                            "{wo_row['description']}"
                        </div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.info('No active work orders logged for this machine in the database.')

elif app_mode == 'AI Maintenance Assistant':
    st.markdown(
        '<p class="main-title">🤖 Generated AI Maintenance Analysis</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        'Generate automated AI maintenance reports and diagnostics using local LLM inference via Ollama.'
    )
    st.markdown('---')

    st.subheader('⚙️ Ollama Configuration')
    cfg_col1, cfg_col2 = st.columns(2)
    with cfg_col1:
        ollama_url = st.text_input(
            'Ollama Endpoint URL:', value='http://localhost:11434/api/generate'
        )
    with cfg_col2:
        model_name = st.text_input('Local Model Name:', value='llama3.2')

    st.markdown('---')
    st.subheader('🛠️ Machine Selection')
    target_pid = st.selectbox(
        'Select Target Machine for Diagnosis:', df['Product ID'].unique()
    )
    selected_m = df[df['Product ID'] == target_pid].iloc[0]
    st.markdown('---')

    if st.button('🚀 Generate AI Maintenance Report', use_container_width=True):
        pid_val = selected_m['Product ID']
        rpm_val = selected_m['Rotational speed [rpm]']
        torque_val = selected_m['Torque [Nm]']
        air_val = selected_m['Air temperature [K]']
        proc_val = selected_m['Process temperature [K]']
        wear_val = selected_m['Tool wear [min]']
        is_fail = selected_m['Machine failure'] == 1

        hidden_prompt = (
            f"Analyze telemetry data for Machine {pid_val}: "
            f"Air Temperature: {air_val}K, Process Temperature: {proc_val}K, "
            f"Rotational Speed: {rpm_val} RPM, Torque: {torque_val} Nm, "
            f"Tool Wear: {wear_val} min, Failure Status: {is_fail}. "
            f"Provide a structured engineering report including risk assessment, anomalous metrics, and concrete actionable maintenance steps."
        )

        with st.spinner('Generating report from Ollama...'):
            try:
                response = requests.post(
                    ollama_url,
                    json={
                        'model': model_name,
                        'prompt': hidden_prompt,
                        'stream': False,
                    },
                    timeout=None,
                )
                if response.status_code == 200 and response.json().get('response'):
                    st.markdown('### 📋 Generated AI Maintenance Analysis')
                    st.info(response.json().get('response').strip())
            except Exception:
                pass

elif app_mode == 'Work Order Console':
    st.markdown(
        '<h2 style="margin-bottom:0px; font-weight:800; color:#ffffff;">Work Order Console</h2>',
        unsafe_allow_html=True,
    )
    st.markdown('<br>', unsafe_allow_html=True)

    tab_registry, tab_create = st.tabs(
        ['📋 Work Order Registry', '➕ Create Work Order']
    )

    with tab_registry:
        wo_df = get_work_orders_df()

        total_wo = len(wo_df)
        open_wo = len(wo_df[wo_df['status'] == 'Open']) if not wo_df.empty else 0
        in_prog_wo = (
            len(wo_df[wo_df['status'] == 'In Progress']) if not wo_df.empty else 0
        )
        completed_wo = (
            len(wo_df[wo_df['status'] == 'Completed']) if not wo_df.empty else 0
        )

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(
                f'''
                <div class="wo-card wo-card-blue">
                    <div class="wo-card-title">TOTAL WORK ORDERS</div>
                    <div class="wo-card-value">{total_wo}</div>
                </div>
                ''',
                unsafe_allow_html=True,
            )
        with m2:
            st.markdown(
                f'''
                <div class="wo-card wo-card-red">
                    <div class="wo-card-title">OPEN REGISTRY TASKS</div>
                    <div class="wo-card-value">{open_wo}</div>
                </div>
                ''',
                unsafe_allow_html=True,
            )
        with m3:
            st.markdown(
                f'''
                <div class="wo-card wo-card-orange">
                    <div class="wo-card-title">ACTIVE REPAIRS</div>
                    <div class="wo-card-value">{in_prog_wo}</div>
                </div>
                ''',
                unsafe_allow_html=True,
            )
        with m4:
            st.markdown(
                f'''
                <div class="wo-card wo-card-green">
                    <div class="wo-card-title">COMPLETED REPAIRS</div>
                    <div class="wo-card-value">{completed_wo}</div>
                </div>
                ''',
                unsafe_allow_html=True,
            )

        st.markdown(
            '<p style="font-size: 12px; font-weight: 800; color: #9ca3af;'
            ' letter-spacing: 0.5px; margin-bottom: 8px;">FILTER & SEARCH REGISTRY</p>',
            unsafe_allow_html=True,
        )

        f1, f2, f3 = st.columns([2, 1, 1])
        with f1:
            search_query = st.text_input(
                'Search',
                placeholder='Search by Machine ID, Assignee, or Description...',
                label_visibility='collapsed',
            )
        with f2:
            status_filter = st.selectbox(
                'Status Filter',
                ['All Statuses', 'Open', 'In Progress', 'Completed'],
                label_visibility='collapsed',
            )
        with f3:
            priority_filter = st.selectbox(
                'Priority Filter',
                ['All Priorities', 'Low', 'Medium', 'High', 'Critical'],
                label_visibility='collapsed',
            )

        filtered_wo = wo_df.copy()
        if not filtered_wo.empty:
            if search_query:
                filtered_wo = filtered_wo[
                    filtered_wo['asset_id'].str.contains(
                        search_query, case=False, na=False
                    )
                    | filtered_wo['technician'].str.contains(
                        search_query, case=False, na=False
                    )
                    | filtered_wo['description'].str.contains(
                        search_query, case=False, na=False
                    )
                ]
            if status_filter != 'All Statuses':
                filtered_wo = filtered_wo[filtered_wo['status'] == status_filter]
            if priority_filter != 'All Priorities':
                filtered_wo = filtered_wo[filtered_wo['priority'] == priority_filter]

        st.markdown('<br>', unsafe_allow_html=True)

        if not filtered_wo.empty:
            reg_left, reg_right = st.columns([1.5, 1.0])

            with reg_left:
                st.markdown(
                    '<p style="font-size: 11px; font-weight: 800; color: #9ca3af; letter-spacing: 0.5px; margin-bottom: 8px;">ACTIVE RECORDS</p>',
                    unsafe_allow_html=True,
                )

                wo_options = {
                    f"Order #{row['id']} - {row['asset_id']} ({row['issue_type']})": (
                        row['id']
                    )
                    for _, row in filtered_wo.iterrows()
                }
                selected_wo_label = st.selectbox(
                    'Select Work Order to Inspect & Manage:', list(wo_options.keys())
                )
                selected_wo_id = wo_options[selected_wo_label]

                st.dataframe(
                    filtered_wo[[
                        'id',
                        'asset_id',
                        'issue_type',
                        'priority',
                        'status',
                        'technician',
                        'due_date',
                    ]],
                    use_container_width=True,
                    height=280,
                )

            with reg_right:
                selected_record = filtered_wo[
                    filtered_wo['id'] == selected_wo_id
                ].iloc[0]

                m_match = df[df['Product ID'] == selected_record['asset_id']]
                m_info = m_match.iloc[0].to_dict() if not m_match.empty else None

                st.markdown(
                    f'''
                    <div class="detail-sheet-box">
                        <h3 style="font-size: 18px; font-weight: 800; margin-bottom: 15px; color: #ffffff;">Order #{selected_record['id']} Detail Sheet</h3>
                    ''',
                    unsafe_allow_html=True,
                )

                st.text_input(
                    'Asset ID:', value=selected_record['asset_id'], disabled=True
                )
                st.text_input(
                    'Issue Category:', value=selected_record['issue_type'], disabled=True
                )

                prio_opts = ['Low', 'Medium', 'High', 'Critical']
                prio_idx = (
                    prio_opts.index(selected_record['priority'])
                    if selected_record['priority'] in prio_opts
                    else 0
                )

                key_prio = f'prio_sel_{selected_wo_id}'
                key_tech = f'tech_inp_{selected_wo_id}'
                key_due = f'due_inp_{selected_wo_id}'
                key_stat = f'stat_sel_{selected_wo_id}'
                key_desc = f'desc_inp_{selected_wo_id}'

                val_prio = st.selectbox(
                    'Priority Level:', prio_opts, index=prio_idx, key=key_prio
                )
                val_tech = st.text_input(
                    'Lead Assignee:',
                    value=selected_record['technician'],
                    key=key_tech,
                )

                try:
                    due_obj = datetime.datetime.strptime(
                        str(selected_record['due_date']), '%Y-%m-%d'
                    ).date()
                except ValueError:
                    due_obj = datetime.date.today()

                val_due = st.date_input('Deadline:', value=due_obj, key=key_due)

                stat_opts = ['Open', 'In Progress', 'Completed']
                stat_idx = (
                    stat_opts.index(selected_record['status'])
                    if selected_record['status'] in stat_opts
                    else 0
                )
                val_stat = st.selectbox(
                    'Current Status:', stat_opts, index=stat_idx, key=key_stat
                )

                val_desc = st.text_area(
                    'Job Description:',
                    value=selected_record['description'],
                    key=key_desc,
                )

                def on_save_click(target_id):
                    update_work_order(
                        target_id,
                        st.session_state[f'prio_sel_{target_id}'],
                        st.session_state[f'tech_inp_{target_id}'],
                        st.session_state[f'due_inp_{target_id}'],
                        st.session_state[f'stat_sel_{target_id}'],
                        st.session_state[f'desc_inp_{target_id}'],
                    )
                    for k in [
                        f'prio_sel_{target_id}',
                        f'tech_inp_{target_id}',
                        f'due_inp_{target_id}',
                        f'stat_sel_{target_id}',
                        f'desc_inp_{target_id}',
                    ]:
                        if k in st.session_state:
                            del st.session_state[k]
                    st.toast('✅ Database Updated Successfully!', icon='🎉')

                def on_delete_click(target_id):
                    delete_work_order(target_id)
                    for k in [
                        f'prio_sel_{target_id}',
                        f'tech_inp_{target_id}',
                        f'due_inp_{target_id}',
                        f'stat_sel_{target_id}',
                        f'desc_inp_{target_id}',
                    ]:
                        if k in st.session_state:
                            del st.session_state[k]
                    st.toast('🗑️ Order Deleted from Database!', icon='🚨')

                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    st.button(
                        '💾 Save Updates',
                        key=f'save_btn_{selected_wo_id}',
                        on_click=on_save_click,
                        args=(selected_wo_id,),
                        use_container_width=True,
                    )
                with btn_col2:
                    st.button(
                        '🗑️ Delete Order',
                        key=f'del_btn_{selected_wo_id}',
                        on_click=on_delete_click,
                        args=(selected_wo_id,),
                        use_container_width=True,
                    )

                st.markdown('<br>', unsafe_allow_html=True)

                pdf_bytes = generate_work_order_pdf(selected_record, m_info)
                st.download_button(
                    label=f"📄 Download Work Order #{selected_record['id']} PDF",
                    data=pdf_bytes,
                    file_name=(
                        f"Work_Order_{selected_record['id']}_{selected_record['asset_id']}.pdf"
                    ),
                    mime='application/pdf',
                    use_container_width=True,
                )

                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info('No work orders found matching the filter criteria.')

    with tab_create:
        st.markdown('#### GENERATE NEW MAINTENANCE TICKET')
        with st.form('create_wo_form'):
            c_col1, c_col2 = st.columns(2)
            with c_col1:
                new_asset = st.selectbox(
                    'Target Machine (Asset ID):', df['Product ID'].unique()
                )
                new_issue = st.selectbox(
                    'Service Classification (Issue Type):',
                    [
                        'Heat Dissipation Failure (HDF)',
                        'Tool Wear Failure (TWF)',
                        'Overstrain Failure (OSF)',
                        'Power Failure (PWF)',
                        'Random Failure (RNF)',
                        'General Maintenance',
                    ],
                )
                new_prio = st.selectbox(
                    'Service Priority:',
                    ['Low', 'Medium', 'High', 'Critical'],
                    index=1,
                )
            with c_col2:
                new_tech = st.text_input('Lead Maintenance Engineer:', value='Alex')
                new_due = st.date_input(
                    'Target Completion Date:', value=datetime.date.today()
                )
                new_status = st.selectbox(
                    'Initial Ticket Status:', ['Open', 'In Progress', 'Completed'], index=0
                )

            new_desc = st.text_area(
                'Maintenance Job Description & Directives:',
                placeholder=(
                    'Outline specific fault symptoms, required tools/LOTO precautions, or component replacement details...'
                ),
            )

            submit_new = st.form_submit_button(
                '📝 Register Maintenance Work Order', use_container_width=True
            )
            if submit_new:
                add_work_order(
                    new_asset,
                    new_issue,
                    new_prio,
                    new_tech,
                    new_due,
                    new_status,
                    new_desc,
                )
                st.success(
                    f'✅ Registered new Work Order for {new_asset} in SQLite database!'
                )
                st.rerun()

elif app_mode == 'Module 7: Preventive Maintenance':
    st.markdown(
        '<h2 style="margin-bottom:0px; font-weight:800; color:#ffffff;">🛠️ Preventive Maintenance</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#9ca3af; font-size:14px;">Automated Preventive Maintenance Scheduling, Frequency Configuration, and Checklist Management</p>',
        unsafe_allow_html=True,
    )
    st.markdown('<br>', unsafe_allow_html=True)

    pm_df = get_pm_schedules_df()

    total_schedules = len(pm_df)
    overdue_count = (
        len(pm_df[pm_df['status'] == 'Overdue']) if not pm_df.empty else 0
    )
    due_today_count = (
        len(pm_df[pm_df['status'] == 'Due Today']) if not pm_df.empty else 0
    )
    active_techs = pm_df['technician'].nunique() if not pm_df.empty else 0

    p1, p2, p3, p4, p5 = st.columns(5)
    with p1:
        st.markdown(
            f'''
            <div class="wo-card wo-card-blue">
                <div class="wo-card-title">TOTAL PM SCHEDULES</div>
                <div class="wo-card-value">{total_schedules}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
    with p2:
        st.markdown(
            f'''
            <div class="wo-card wo-card-red">
                <div class="wo-card-title">OVERDUE SCHEDULES</div>
                <div class="wo-card-value">{overdue_count}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
    with p3:
        st.markdown(
            f'''
            <div class="wo-card wo-card-orange">
                <div class="wo-card-title">DUE TODAY</div>
                <div class="wo-card-value">{due_today_count}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
    with p4:
        st.markdown(
            f'''
            <div class="wo-card wo-card-purple">
                <div class="wo-card-title">ASSIGNED TECHS</div>
                <div class="wo-card-value">{active_techs}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
    with p5:
        st.markdown(
            '''
            <div class="wo-card wo-card-green">
                <div class="wo-card-title">PM HEALTH SCORE</div>
                <div class="wo-card-value">94.2%</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

    st.markdown('<br>', unsafe_allow_html=True)

    tab_pm_cal, tab_pm_add, tab_checklist, tab_pm_ai = st.tabs([
        '📅 PM Calendar & Schedules',
        '⚙️ Configure Frequency & Schedule',
        '📋 Maintenance Checklist & Status',
        '🤖 AI PM Recommendations',
    ])

    with tab_pm_cal:
        st.markdown('#### PREVENTIVE MAINTENANCE SCHEDULES & CALENDAR TRACKER')

        c_filter, c_search = st.columns([1, 2])
        with c_filter:
            pm_status_filter = st.selectbox(
                'Filter Status:',
                ['All', 'Overdue', 'Due Today', 'Scheduled', 'Completed'],
            )
        with c_search:
            pm_search = st.text_input(
                'Search PM Tasks or Asset IDs:',
                placeholder='Enter Asset ID or Task Name...',
            )

        disp_pm_df = pm_df.copy()
        if pm_status_filter != 'All':
            disp_pm_df = disp_pm_df[disp_pm_df['status'] == pm_status_filter]
        if pm_search:
            disp_pm_df = disp_pm_df[
                disp_pm_df['asset_id'].str.contains(pm_search, case=False, na=False)
                | disp_pm_df['task_name'].str.contains(
                    pm_search, case=False, na=False
                )
                | disp_pm_df['technician'].str.contains(
                    pm_search, case=False, na=False
                )
            ]

        st.dataframe(
            disp_pm_df[[
                'id',
                'asset_id',
                'task_name',
                'frequency',
                'technician',
                'last_performed',
                'next_due',
                'status',
            ]],
            use_container_width=True,
            height=260,
        )

        st.markdown('---')
        st.markdown('#### ⚡ GENERATE PREVENTIVE WORK ORDER FROM SCHEDULE')
        if not disp_pm_df.empty:
            gen_col1, gen_col2 = st.columns([3, 1])
            with gen_col1:
                sel_pm_label = st.selectbox(
                    'Select PM Task to Convert into Active Work Order:', [
                        (
                            f"PM #{r['id']} - {r['asset_id']}: {r['task_name']}"
                            f" ({r['status']})"
                        )
                        for _, r in disp_pm_df.iterrows()
                    ]
                )
                sel_pm_id = int(sel_pm_label.split(' - ')[0].replace('PM #', ''))
                selected_pm_row = pm_df[pm_df['id'] == sel_pm_id].iloc[0]
            with gen_col2:
                st.markdown('<br>', unsafe_allow_html=True)
                if st.button(
                    '🚀 Generate Preventive Work Order', use_container_width=True
                ):
                    add_work_order(
                        asset_id=selected_pm_row['asset_id'],
                        issue_type='Preventive Maintenance',
                        priority=(
                            'High'
                            if selected_pm_row['status'] in ['Overdue', 'Due Today']
                            else 'Medium'
                        ),
                        technician=selected_pm_row['technician'],
                        due_date=selected_pm_row['next_due'],
                        status='Open',
                        description=(
                            'Preventive Work Order generated for'
                            f" {selected_pm_row['task_name']}. Frequency:"
                            f" {selected_pm_row['frequency']}. Checklist:"
                            f" {selected_pm_row['checklist']}"
                        ),
                    )
                    st.toast(
                        '✅ Generated Work Order for Asset'
                        f" {selected_pm_row['asset_id']} in database!",
                        icon='🎉',
                    )

    with tab_pm_add:
        st.markdown('#### CONFIGURE NEW PREVENTIVE MAINTENANCE SCHEDULE')
        with st.form('create_pm_form'):
            pm_col1, pm_col2 = st.columns(2)
            with pm_col1:
                pm_asset = st.selectbox(
                    'Select Target Asset ID:', df['Product ID'].unique()
                )
                pm_task = st.text_input(
                    'Maintenance Task Name:',
                    value='Spindle Assembly Lubrication & Thermal Scan',
                )
                pm_freq = st.selectbox(
                    'Configured Maintenance Frequency:',
                    [
                        'Daily',
                        'Weekly',
                        'Bi-Weekly',
                        'Monthly',
                        'Quarterly',
                        'Semi-Annual',
                        'Annual',
                    ],
                )
            with pm_col2:
                pm_tech = st.text_input('Assigned Lead Technician:', value='Alex')
                pm_last = st.date_input(
                    'Last Performed Date:',
                    value=datetime.date.today() - datetime.timedelta(days=14),
                )

                freq_days = {
                    'Daily': 1,
                    'Weekly': 7,
                    'Bi-Weekly': 14,
                    'Monthly': 30,
                    'Quarterly': 90,
                    'Semi-Annual': 180,
                    'Annual': 365,
                }
                calculated_due = pm_last + datetime.timedelta(
                    days=freq_days.get(pm_freq, 30)
                )

                pm_next = st.date_input(
                    'Calculated Next Due Date:', value=calculated_due
                )

            pm_checklist = st.text_area(
                'Maintenance Checklist Directives:',
                value=(
                    '1. Lockout/Tagout machine power line.\n2. Clean spindle casing'
                    ' and inspect for metal shavings.\n3. Measure thermal gradient'
                    ' across bearing housings.\n4. Apply grease to drive couplings.'
                ),
            )

            submit_pm = st.form_submit_button(
                '💾 Save & Deploy PM Schedule', use_container_width=True
            )
            if submit_pm:
                calc_status = (
                    'Overdue'
                    if pm_next < datetime.date.today()
                    else (
                        'Due Today'
                        if pm_next == datetime.date.today()
                        else 'Scheduled'
                    )
                )
                add_pm_schedule(
                    pm_asset,
                    pm_task,
                    pm_freq,
                    pm_tech,
                    pm_last,
                    pm_next,
                    calc_status,
                    pm_checklist,
                )
                st.success(
                    f'✅ Preventive Maintenance Schedule configured for {pm_asset}!'
                )
                st.rerun()

    with tab_checklist:
        st.markdown('#### MAINTENANCE CHECKLIST & EXECUTION STATUS')
        if not pm_df.empty:
            chk_pm_label = st.selectbox(
                'Select Active Maintenance Schedule:', [
                    (
                        f"PM #{r['id']} - {r['asset_id']}: {r['task_name']}"
                        f" ({r['status']})"
                    )
                    for _, r in pm_df.iterrows()
                ],
                key='chk_pm_select',
            )
            chk_pm_id = int(chk_pm_label.split(' - ')[0].replace('PM #', ''))
            chk_row = pm_df[pm_df['id'] == chk_pm_id].iloc[0]

            st.markdown(
                f"""
                <div style="background-color: #1f2937; border: 1px solid #374151; border-radius: 8px; padding: 18px; margin-bottom: 20px;">
                    <b>Asset ID:</b> {chk_row['asset_id']} &nbsp;|&nbsp; 
                    <b>Task:</b> {chk_row['task_name']} &nbsp;|&nbsp; 
                    <b>Frequency:</b> {chk_row['frequency']} &nbsp;|&nbsp; 
                    <b>Assigned Tech:</b> {chk_row['technician']} &nbsp;|&nbsp; 
                    <b>Status:</b> <span style="font-weight:bold; color:{'#ef4444' if chk_row['status']=='Overdue' else '#10b981'};">{chk_row['status']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown('##### 📝 Active Maintenance Checklist Items')
            checklist_items = (
                chk_row['checklist'].split('\n')
                if chk_row['checklist']
                else ['No specific checklist provided.']
            )

            completed_steps = 0
            for i, item in enumerate(checklist_items):
                if item.strip():
                    checked = st.checkbox(
                        f'{item.strip()}', key=f'chk_item_{chk_pm_id}_{i}'
                    )
                    if checked:
                        completed_steps += 1

            progress_pct = completed_steps / max(len(checklist_items), 1)
            st.progress(progress_pct)
            st.caption(
                f'Checklist Completion Progress: {int(progress_pct * 100)}%'
            )

            st.markdown('<br>', unsafe_allow_html=True)
            if st.button(
                '✅ Mark Maintenance Complete & Update Next Due Date',
                use_container_width=True,
            ):
                new_last = datetime.date.today()
                freq_days = {
                    'Daily': 1,
                    'Weekly': 7,
                    'Bi-Weekly': 14,
                    'Monthly': 30,
                    'Quarterly': 90,
                    'Semi-Annual': 180,
                    'Annual': 365,
                }
                new_next = new_last + datetime.timedelta(
                    days=freq_days.get(chk_row['frequency'], 30)
                )

                update_pm_status(chk_pm_id, 'Scheduled', new_last, new_next)
                st.toast(
                    f"🎉 PM Task for {chk_row['asset_id']} completed! Next due date set to {new_next}.",
                    icon='✅',
                )
                st.rerun()

    with tab_pm_ai:
        st.markdown('#### 🤖 AI-BASED PREVENTIVE MAINTENANCE RECOMMENDATIONS')
        st.markdown(
            'Local AI diagnostic engine analyzes high-wear assets and suggests dynamic frequency adjustments.'
        )
        st.markdown('---')

        high_wear_machines = df[df['Tool wear [min]'] > 180]

        st.markdown(
            '**High-Wear Asset Count Identified:** `'
            f'{len(high_wear_machines)} machines exceeding 180 tool wear minutes`'
        )

        if not high_wear_machines.empty:
            st.markdown('##### Recommended PM Frequency Adjustments')
            rec_data = []
            for _, hw_row in high_wear_machines.head(5).iterrows():
                rec_data.append({
                    'Asset ID': hw_row['Product ID'],
                    'Machine Type': hw_row['Type'],
                    'Tool Wear (min)': hw_row['Tool wear [min]'],
                    'Current Frequency': 'Monthly',
                    'AI Recommended Frequency': 'Bi-Weekly (Increase Frequency 2x)',
                    'Action Directive': (
                        'Dynamic vibration analysis & spindle bearing grease replenishment recommended due to high cumulative wear.'
                    ),
                })
            st.dataframe(pd.DataFrame(rec_data), use_container_width=True)

            st.info(
                '💡 **AI Insight:** Increasing PM frequency for high-wear assets prevents unpredicted Overstrain (OSF) and Tool Wear (TWF) failures before they impact shop-floor productivity.'
            )