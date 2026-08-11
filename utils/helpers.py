import pandas as pd


# -----------------------------
# Load Dataset
# -----------------------------

def load_dataset():
    return pd.read_csv("data/ai4i2020.csv")


# -----------------------------
# Machine Health
# -----------------------------

def machine_health(machine):

    if machine["Machine failure"] == 1:
        return "🔴 Critical"

    elif machine["Tool wear [min]"] > 180:
        return "🟡 Warning"

    return "🟢 Healthy"


# -----------------------------
# Risk Level
# -----------------------------

def risk_level(machine):

    if machine["Machine failure"] == 1:
        return "🔴 Critical Risk"

    elif machine["Tool wear [min]"] > 200:
        return "🟠 High Risk"

    elif (
        machine["Torque [Nm]"] > 55 or
        machine["Process temperature [K]"] > 310
    ):
        return "🟡 Medium Risk"

    return "🟢 Low Risk"


# -----------------------------
# Failure Types
# -----------------------------

def detected_failures(machine):

    mapping = {
        "TWF": "Tool Wear Failure",
        "HDF": "Heat Dissipation Failure",
        "PWF": "Power Failure",
        "OSF": "Overstrain Failure",
        "RNF": "Random Failure"
    }

    failures = []

    for key, value in mapping.items():

        if machine[key] == 1:
            failures.append(value)

    return failures


# -----------------------------
# Recommendation
# -----------------------------

def recommendations(machine):

    rec = []

    if machine["Machine failure"] == 1:
        rec.append("Immediate maintenance required.")

    if machine["Tool wear [min]"] > 200:
        rec.append("Replace cutting tool.")

    if machine["Torque [Nm]"] > 55:
        rec.append("Inspect drive system.")

    if machine["Process temperature [K]"] > 310:
        rec.append("Check cooling system.")

    if machine["Rotational speed [rpm]"] > 1600:
        rec.append("Inspect spindle speed.")

    if len(rec) == 0:
        rec.append("Machine operating normally.")

    return rec