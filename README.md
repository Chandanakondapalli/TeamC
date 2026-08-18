# 🤖 Agentic AI for Smart Facility Operations and Optimization

> **An AI-powered facility maintenance platform for machine health analysis, predictive and preventive maintenance, intelligent recommendations, and work-order management.**

---

## 📌 About the Project

**Agentic AI for Smart Facility Operations and Optimization** is an intelligent facility maintenance platform developed using **Python and Streamlit**.

The platform combines **machine data analysis, facility monitoring, machine-level health analysis, Generative AI, preventive maintenance, and work-order management** into a unified system.

The main purpose of the project is to help maintenance teams understand machine conditions, identify potential maintenance risks, receive AI-assisted recommendations, and convert maintenance requirements into actionable work orders.

The platform follows an end-to-end maintenance workflow:

```text
Machine Data
     ↓
Data Analysis
     ↓
Facility Dashboard
     ↓
Machine Explorer
     ↓
AI Maintenance Assessment
     ↓
Maintenance Recommendation
     ↓
Work Order Creation
     ↓
Work Order Management
     ↓
Technician Execution
```

---

# 🎯 Objectives

The project aims to:

* Analyze industrial machine data
* Monitor machine health and operating conditions
* Identify machine failures and risk factors
* Provide facility-level maintenance insights
* Generate AI-assisted maintenance assessments
* Support predictive maintenance decisions
* Support preventive maintenance activities
* Create maintenance work orders
* Manage and track work orders
* Connect maintenance recommendations with technician activities
* Provide a centralized facility maintenance workflow

---

# ✨ Key Features

## 📊 1. Data Analysis

The Data Analysis module performs **Exploratory Data Analysis (EDA)** on the machine dataset.

It provides analysis such as:

* Dataset overview
* Data statistics
* Missing-value analysis
* Duplicate-value analysis
* Machine failure analysis
* Machine type analysis
* Sensor distributions
* Correlation analysis
* Temperature analysis
* RPM analysis
* Torque analysis
* Tool-wear analysis
* Failure-type analysis

The analysis helps identify patterns and relationships between machine operating parameters and machine failures.

---

# 📈 2. Facility Dashboard

The Dashboard provides an overall view of machine and facility conditions.

### Key Performance Indicators

The dashboard displays important metrics such as:

* Total Machines
* Healthy Machines
* Failed Machines
* Failure Rate
* Average RPM
* Average Tool Wear

### Visual Analytics

The dashboard includes:

* Machine Failure Distribution
* Machine Type Distribution
* RPM Distribution
* Tool Wear Distribution
* RPM vs Torque
* Air Temperature vs Process Temperature
* Tool Wear vs Machine Failure
* Torque vs Machine Failure
* Failure-Type Analysis
* Correlation Heatmap

Users can apply filters to analyze machines based on their **status** and **machine type**.

---

# 🔍 3. Machine Explorer

The Machine Explorer allows users to investigate individual machines.

Users can search/select a machine using its **Product ID**.

### Machine information includes:

* Product ID
* Machine Type
* Air Temperature
* Process Temperature
* Rotational Speed
* Torque
* Tool Wear
* Machine Failure
* Failure Indicators
* Machine Health Status

This module allows users to move from a facility-level overview to detailed machine-level analysis.

---

# 🤖 4. AI Maintenance Assistant

The AI Maintenance Assistant is the intelligence layer of the platform.

It analyzes machine information and generates an AI-assisted maintenance assessment using **Google Gemini AI**.

### AI-generated information can include:

* Machine Status
* Risk Status
* Maintenance Report
* Sensor Analysis
* Failure Analysis
* Maintenance Recommendations
* Priority
* Next Inspection
* Conclusion

The assistant converts machine information into understandable maintenance guidance that can support maintenance decision-making.

### AI Maintenance Workflow

```text
Machine Information
        ↓
Machine Health Analysis
        ↓
AI Assessment
        ↓
Risk Evaluation
        ↓
Maintenance Recommendation
        ↓
Work Order
```

---

# 🛠️ 5. Preventive Maintenance

The platform supports **preventive maintenance** in addition to AI-assisted predictive maintenance.

Preventive maintenance allows maintenance activities to be planned based on scheduled requirements.

A preventive maintenance requirement can contain information such as:

* Machine
* Maintenance activity
* Schedule
* Priority
* Due date
* Technician
* Maintenance requirements

### Preventive Maintenance → Work Order

```text
Preventive Maintenance Schedule
             ↓
Maintenance Requirement
             ↓
Work Order Creation
```

This ensures that planned maintenance activities can also enter the operational work-order workflow.

---

# 📝 6. Work Order Creation

The Work Orders module converts maintenance requirements into actionable maintenance tasks.

Work orders can originate from **two major sources**:

### AI-Assisted Maintenance

```text
Machine Analysis
      ↓
AI Recommendation
      ↓
Work Order
```

### Preventive Maintenance

```text
Maintenance Schedule
      ↓
Maintenance Requirement
      ↓
Work Order
```

Both workflows connect to the same Work Order Management system.

### Work Order Information

A work order can contain:

* Work Order ID
* Machine ID
* Machine Type
* Priority
* Maintenance Type
* Technician
* Status
* Created Date
* Due Date
* Estimated Cost
* Estimated Time
* Description

The AI-assisted workflow can prefill relevant work-order information based on the maintenance assessment.

---

# 📋 7. Work Order Management

Work Order Creation and Work Order Management are implemented within the same application module.

The system allows users to:

* View work orders
* Search work orders
* Filter work orders
* Create work orders
* Update work-order status
* Edit work-order information
* Delete work orders
* View work-order details
* Monitor work-order KPIs
* Track maintenance activities

### Work Order Status

The system supports maintenance states such as:

```text
Open
   ↓
In Progress
   ↓
Completed
```

This provides visibility into the progress of maintenance activities.

---

# 👨‍🔧 8. Technician Workflow

The platform connects work orders with technician activities.

The overall workflow is:

```text
Work Order
     ↓
Technician Assignment
     ↓
Technician View
     ↓
Maintenance Activity
     ↓
Status Update
     ↓
Completed
```

This connects the maintenance decision with the actual execution of the maintenance task.

---

# 🔄 Complete Maintenance Workflow

The complete platform workflow can be represented as:

```text
                    MACHINE DATA
                         │
                         ▼
                 ┌───────────────┐
                 │ Data Analysis │
                 └───────┬───────┘
                         │
                         ▼
                  ┌────────────┐
                  │ Dashboard  │
                  └─────┬──────┘
                        │
                        ▼
              ┌──────────────────┐
              │ Machine Explorer │
              └────────┬─────────┘
                       │
                       ▼
          ┌─────────────────────────┐
          │ AI Maintenance Assistant│
          └────────────┬────────────┘
                       │
                       ▼
             Maintenance Decision
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
       AI Recommendation   Preventive
              │            Maintenance
              │                 │
              └────────┬────────┘
                       ▼
                Work Order
                   Creation
                       │
                       ▼
              Work Order Management
                       │
                       ▼
               Technician Workflow
                       │
                       ▼
                  Maintenance
                   Execution
```

---

# 🏗️ System Architecture

The application consists of several interconnected layers.

```text
┌─────────────────────────────────────────────┐
│             Streamlit Application           │
├─────────────────────────────────────────────┤
│                                             │
│  Data Analysis                              │
│  Dashboard                                  │
│  Machine Explorer                           │
│  AI Maintenance Assistant                  │
│  Preventive Maintenance                     │
│  Work Orders                                │
│  Technician Workflow                        │
│                                             │
└──────────────────────┬──────────────────────┘
                       │
          ┌────────────┼─────────────┐
          │            │             │
          ▼            ▼             ▼
     Data Layer     AI Layer    Database Layer
          │            │             │
          ▼            ▼             ▼
     AI4I Dataset  Gemini AI      SQLite
```

### Data Layer

Handles machine data and data analysis.

### AI Layer

Uses Gemini AI to generate machine maintenance assessments and recommendations.

### Database Layer

Stores operational maintenance and work-order information.

### Application Layer

Provides the interactive Streamlit interface through multiple modules.

---

# 🧠 AI-Based Maintenance Intelligence

The AI component is designed to transform machine information into maintenance-oriented insights.

The workflow combines machine parameters and machine-health information before generating a structured maintenance assessment.

The AI output is intended to support:

* Machine health understanding
* Risk identification
* Maintenance prioritization
* Maintenance recommendations
* Inspection planning
* Work-order preparation

The AI assistant therefore acts as a bridge between **machine data and maintenance operations**.

---

# 📊 Dataset

The project uses the **AI4I 2020 Predictive Maintenance Dataset**.

The dataset contains machine information including:

* UDI
* Product ID
* Type
* Air Temperature
* Process Temperature
* Rotational Speed
* Torque
* Tool Wear
* Machine Failure
* TWF
* HDF
* PWF
* OSF
* RNF

These attributes are used for data analysis, visualization, machine exploration, and maintenance assessment.

---

# 🛠️ Technology Stack

### Programming

* Python
* SQL

### Application

* Streamlit

### Data Processing

* Pandas
* NumPy

### Data Visualization

* Matplotlib
* Seaborn

### Artificial Intelligence

* Google Gemini AI
* Generative AI
* Prompt Engineering

### Database

* SQLite

### Development Tools

* Git
* GitHub
* VS Code
* Ubuntu/Linux

---

# 📂 Project Structure

The project uses a Streamlit multi-page architecture with reusable utility modules.

```text
Agentic_FacilityOps_AI/
│
├── data/
│   └── ai4i2020.csv
│
├── pages/
│   ├── 1_📊_Data_Analysis.py
│   ├── 2_📈_Dashboard.py
│   ├── 3_🔍_Machine_Explorer.py
│   ├── 4_🤖_AI_Maintenance_Assistant.py
│   ├── 5_📝_Work_Orders.py
│   └── ...
│
├── utils/
│   ├── ai_report.py
│   ├── database.py
│   ├── charts.py
│   ├── cards.py
│   ├── theme.py
│   ├── ui.py
│   └── ...
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

> The structure above represents the main organization of the project. Additional modules and files may be present as the application evolves.

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/PavaniPerisetla/Agentic_AI_for_Smart_Facility_Operations_and_Optimization.git
```

## 2. Navigate to the project

Your **GitHub repository name** and your **local project-folder name** are different.

The local project folder is:

```bash
cd Agentic_FacilityOps_AI
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Gemini AI

The AI Maintenance Assistant requires a Gemini API key.

Configure the API key using the application's environment/secrets configuration.

**Do not commit API keys or credentials to GitHub.**

## 5. Run the application

```bash
streamlit run app.py
```

---

# 🔐 Security

Sensitive configuration should not be committed to the repository.

Recommended `.gitignore` entries:

```gitignore
__pycache__/
*.pyc
.env
.streamlit/secrets.toml
*.db
*.sqlite
*.sqlite3
```

Never upload:

* API keys
* Passwords
* Authentication credentials
* Private tokens
* Sensitive database files

---

# 📌 Project Highlights

### 🔹 Data-Driven

Machine sensor data is analyzed to identify operating patterns and failure-related conditions.

### 🔹 AI-Assisted

Gemini AI converts machine information into maintenance-oriented assessments and recommendations.

### 🔹 Preventive Maintenance

The system supports planned maintenance activities in addition to AI-assisted maintenance recommendations.

### 🔹 Operational

Maintenance recommendations and preventive maintenance requirements can be converted into actual work orders.

### 🔹 Trackable

Work orders can be searched, filtered, updated, and managed throughout their lifecycle.

### 🔹 Integrated

The platform connects machine analysis, AI intelligence, maintenance planning, and technician execution in one workflow.

---

# 💡 Benefits

The platform helps maintenance teams:

* Understand machine health more easily
* Identify potential maintenance risks
* Make data-driven maintenance decisions
* Reduce dependence on reactive maintenance
* Support preventive maintenance planning
* Generate maintenance work orders efficiently
* Track maintenance activities
* Centralize facility maintenance operations

---

# 🔮 Future Scope

Future enhancements can include:

* Real-time IoT sensor integration
* Live machine monitoring
* Advanced machine-learning-based failure prediction
* Automated preventive-maintenance scheduling
* Real-time maintenance alerts
* Maintenance cost prediction
* RAG-based maintenance knowledge assistant
* Multi-agent maintenance coordination
* Cloud deployment
* Advanced technician optimization
* Enterprise CMMS integration

---

# 👩‍💻 Developer

**Pavani Perisetla**

B.Tech — Computer Science and Engineering

---

# 📄 License

This project is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for details.

---

# ⭐ Project Summary

**Agentic AI for Smart Facility Operations and Optimization** brings together machine data analysis, facility monitoring, AI-assisted maintenance intelligence, preventive maintenance, and work-order management.

The platform follows a simple operational principle:

```text
Analyze
   ↓
Understand
   ↓
Predict
   ↓
Recommend
   ↓
Create
   ↓
Execute
   ↓
Track
```

> **From machine data to intelligent maintenance action.**
