# 🤖 Agentic FacilityOps AI Platform

An **AI-powered facility maintenance and operations platform** designed to monitor machine health, analyze equipment failures, assist maintenance teams with AI-generated insights, and manage maintenance work orders.

The platform combines **predictive maintenance, data analytics, machine monitoring, and Agentic AI** to help maintenance teams identify potential machine problems and take preventive action.

---

## 🚀 Project Overview

Traditional facility maintenance often depends on manual monitoring and reactive maintenance after equipment failures occur.

**Agentic FacilityOps AI Platform** provides a centralized system where users can:

* 📊 Analyze machine and maintenance data
* 🏭 Monitor individual machine health
* ⚠️ Identify machine failures and risk factors
* 🤖 Get AI-assisted maintenance recommendations
* 🔧 Create and manage maintenance work orders
* 📈 Explore sensor data and failure patterns
* 🛠️ Support preventive and predictive maintenance

---

## ✨ Key Features

### 📊 1. Interactive Dashboard

Provides an overview of facility and machine performance through interactive analytics.

**Dashboard includes:**

* Total Machines
* Machine Failures
* Healthy Machines
* Average RPM
* Failure Rate
* Machine failure distribution
* Machine type analysis
* RPM vs Torque analysis
* Tool wear analysis
* Air temperature trends

---

### 🏭 2. Machine Explorer

Allows users to search and inspect individual machines using their **Product ID**.

Users can view:

* Machine information
* Air temperature
* Process temperature
* Rotational speed
* Torque
* Tool wear
* Machine failure status
* Failure type
* Machine health status

---

### 🤖 3. AI Maintenance Assistant

The AI Maintenance Assistant analyzes machine information and provides maintenance insights.

It can generate:

* Machine health summary
* Sensor analysis
* Failure analysis
* Risk level
* Maintenance recommendation
* Maintenance priority
* Next inspection recommendation

This helps maintenance teams make faster and more informed decisions.

---

### 🔧 4. Maintenance Work Orders

The platform supports maintenance work-order management.

Users can create work orders with:

* Maintenance issue
* Priority
* Assigned technician
* Due date
* Work-order state

The system provides confirmation when a work order is successfully created.

---

### 📈 5. EDA Analysis

Exploratory Data Analysis helps identify relationships and patterns in machine sensor data.

The analysis includes:

* Temperature patterns
* RPM distribution
* Torque analysis
* Tool wear analysis
* Machine failure patterns
* Machine type comparison

---

## 🧠 Agentic AI Workflow

The platform follows an AI-assisted maintenance workflow:

```text
Machine Sensor Data
        ↓
Data Processing & Analysis
        ↓
Machine Health Evaluation
        ↓
Failure / Risk Detection
        ↓
AI Maintenance Assistant
        ↓
Maintenance Recommendation
        ↓
Work Order Creation
        ↓
Maintenance Action
```

The goal is to move from **reactive maintenance** toward **predictive and preventive maintenance**.

---

## 🏗️ Project Architecture

```text
                    ┌─────────────────────┐
                    │   Machine Dataset   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Data Processing     │
                    │ & EDA Analysis      │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │      FacilityOps Dashboard      │
              └───────────────┬────────────────┘
                              │
             ┌────────────────┼─────────────────┐
             │                │                 │
             ▼                ▼                 ▼
      Dashboard        Machine Explorer    EDA Analysis
             │                │
             │                ▼
             │       Machine Health Analysis
             │                │
             │                ▼
             │       AI Maintenance Assistant
             │                │
             │                ▼
             │       Maintenance Recommendation
             │                │
             └────────────────┼─────────────────┐
                              ▼                 │
                       Work Order System ◄──────┘
```

---

## 🛠️ Technologies Used

### Programming Languages

* Python
* SQL
* HTML
* CSS

### Data & Analytics

* Pandas
* NumPy
* Matplotlib
* Plotly
* Exploratory Data Analysis

### AI / Machine Learning

* Generative AI
* Large Language Models
* AI-assisted maintenance analysis
* Predictive maintenance concepts
* Ollama / Local LLM integration

### Application Development

* Streamlit
* SQLite

### Development Tools

* Git
* GitHub
* VS Code
```

> Update the structure above if your actual project contains different files or folders.

---

## 📊 Dataset

The project uses the **AI4I 2020 Predictive Maintenance Dataset** for machine monitoring and predictive maintenance analysis.

The dataset contains machine sensor information such as:

* Product Type
* Air Temperature
* Process Temperature
* Rotational Speed
* Torque
* Tool Wear
* Machine Failure
* Failure Type Indicators

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Chandanakondapalli/agentic-facilityops-ai-platform.git
```

### 2. Navigate to the project

```bash
cd agentic-facilityops-ai-platform
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

If your main application is `app.py`:

```bash
streamlit run app.py
```

If your dashboard is `dashboard.py`:

```bash
streamlit run dashboard.py
```

The application will open in your browser.

---


## 🎯 Project Objectives

* Reduce unexpected machine failures
* Improve preventive maintenance
* Monitor machine health
* Identify potential equipment risks
* Provide AI-assisted maintenance recommendations
* Improve maintenance decision-making
* Centralize facility maintenance operations

---

## 🔮 Future Enhancements

* Real-time IoT sensor integration
* Advanced predictive failure models
* Automated work-order generation
* Technician assignment optimization
* Real-time maintenance alerts
* RAG-based maintenance knowledge assistant
* Role-based access control
* Cloud deployment
* Maintenance cost prediction
* Historical maintenance analytics

---

## 👩‍💻 Developed By

**Kondapalli Sai Chandana**

Bachelor of Engineering — Artificial Intelligence & Data Science

**Ramachandra College of Engineering**

---

## 📄 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.
