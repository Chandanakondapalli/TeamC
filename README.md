# 🏭 Predictive Maintenance System

An AI-powered predictive maintenance platform for monitoring machine
conditions, analyzing sensor data, predicting machine failures, and
managing maintenance work orders.

## 📌 Project Overview

The Predictive Maintenance System helps maintenance teams monitor
industrial machines and manage maintenance operations efficiently.

The system provides:

- Machine monitoring
- Sensor data analysis
- Machine failure analysis
- AI-powered maintenance assistance
- Work order creation and management
- Technician assignment
- Preventive maintenance management
- Role-based access for administrators and technicians

## 🚀 Features

### 👤 User Authentication

The system provides role-based authentication for:

- Administrator
- Technician

Each user receives access according to their assigned role.

### 🏭 Machine Explorer

Allows users to:

- Search machines
- View machine information
- View sensor readings
- Analyze machine health
- Identify machine failure conditions

### 🤖 AI Maintenance Assistant

Provides AI-powered maintenance recommendations based on
machine information and sensor conditions.

### 📋 Work Order Management

Administrators can:

- Create work orders
- Assign technicians
- Set priorities
- Update work order status
- Monitor maintenance activities

Technicians can view and manage work orders assigned to them.

### 🗓️ Preventive Maintenance

Provides maintenance scheduling features including:

- Maintenance schedules
- Technician assignment
- Upcoming tasks
- Overdue tasks
- Maintenance tracking

## 📊 Dataset

The project uses the AI4I 2020 Predictive Maintenance Dataset.

The dataset contains machine sensor information and machine
failure indicators used for predictive maintenance analysis.

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Scikit-learn
- Ollama
- SQLite

## 📁 Project Structure

text
Predictive-Maintenance/
│
├── Login.py
├── Home.py
├── login_database.py
├── work_order_database.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── .streamlit/
│   └── secrets.toml.example
│
├── pages/
│
└── dataset/
    └── ai4i2020.csv