"""
==========================================================
AI Maintenance Report Generator
Agentic FacilityOps AI Platform
==========================================================

This module:
• Calculates engineering metrics
• Evaluates machine health
• Generates AI maintenance reports using Gemini
• Returns report and work order information
"""

import math
import os
from datetime import datetime

from dotenv import load_dotenv
from google import genai

# ---------------------------------------------------------
# Gemini Configuration
# ---------------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


# ==========================================================
# Engineering Calculations
# ==========================================================

def estimated_power_kw(rpm, torque):
    """
    Mechanical Power (kW)

    P = 2πNT / 60000
    """
    return round((2 * math.pi * rpm * torque) / 60000, 2)


def temperature_difference(air_temp, process_temp):
    """
    Temperature Difference
    """
    return round(process_temp - air_temp, 2)


# ==========================================================
# Tool Condition
# ==========================================================

def tool_condition(tool_wear):

    if tool_wear <= 50:
        return "New"

    elif tool_wear <= 120:
        return "Good"

    elif tool_wear <= 180:
        return "Moderate Wear"

    elif tool_wear <= 240:
        return "High Wear"

    return "Critical Wear"


# ==========================================================
# Thermal Status
# ==========================================================

def thermal_status(delta):

    if 8 <= delta <= 12:
        return "Healthy"

    elif delta <= 15:
        return "Warning"

    return "Critical"


# ==========================================================
# Remaining Useful Life
# ==========================================================

def remaining_useful_life(tool_wear):

    if tool_wear < 50:
        return 200

    elif tool_wear < 120:
        return 160

    elif tool_wear < 180:
        return 120

    elif tool_wear < 240:
        return 60

    return 20


# ==========================================================
# Health Score
# ==========================================================

def health_score(machine):

    score = 100

    score -= min(machine["Tool wear [min]"] / 8, 25)

    if machine["Machine failure"] == 1:
        score -= 30

    failures = [
        machine["TWF"],
        machine["HDF"],
        machine["PWF"],
        machine["OSF"],
        machine["RNF"]
    ]

    score -= sum(failures) * 10

    delta = temperature_difference(
        machine["Air temperature [K]"],
        machine["Process temperature [K]"]
    )

    if delta > 12:
        score -= (delta - 12) * 2

    return max(0, round(score))


# ==========================================================
# Risk Level
# ==========================================================

def risk_level(score):

    if score >= 90:
        return "Low"

    elif score >= 75:
        return "Medium"

    elif score >= 60:
        return "High"

    return "Critical"


# ==========================================================
# Priority
# ==========================================================

def maintenance_priority(risk):

    priorities = {
        "Low": "Low",
        "Medium": "Medium",
        "High": "High",
        "Critical": "Critical"
    }

    return priorities[risk]


# ==========================================================
# Estimated Maintenance Cost
# ==========================================================

def maintenance_cost(risk):

    costs = {
        "Low": "2,500",
        "Medium": "8,000",
        "High": "20,000",
        "Critical": "50,000"
    }

    return costs[risk]


# ==========================================================
# Engineering Summary
# ==========================================================

def engineering_summary(machine):

    delta = temperature_difference(
        machine["Air temperature [K]"],
        machine["Process temperature [K]"]
    )

    power = estimated_power_kw(
        machine["Rotational speed [rpm]"],
        machine["Torque [Nm]"]
    )

    score = health_score(machine)

    risk = risk_level(score)

    return {

        "health_score": score,

        "risk": risk,

        "priority": maintenance_priority(risk),

        "maintenance_cost": maintenance_cost(risk),

        "estimated_power": power,

        "delta_temperature": delta,

        "tool_condition": tool_condition(
            machine["Tool wear [min]"]
        ),

        "thermal_status": thermal_status(delta),

        "remaining_life": remaining_useful_life(
            machine["Tool wear [min]"]
        )

    }

# ==========================================================
# Generate Complete Machine Report
# ==========================================================

def generate_machine_report(machine):

    try:

        # --------------------------------------------------
        # Engineering Analysis
        # --------------------------------------------------

        eng = engineering_summary(machine)

        # --------------------------------------------------
        # Prompt
        # --------------------------------------------------

        prompt = f"""
You are a Senior Predictive Maintenance Engineer specializing in industrial machinery and facility operations.

Generate a professional predictive maintenance report using ONLY the information provided below.

==================================================
MACHINE INFORMATION
==================================================

Machine ID : {machine["Product ID"]}
Machine Type : {machine["Type"]}

Air Temperature : {machine["Air temperature [K]"]:.2f} K
Process Temperature : {machine["Process temperature [K]"]:.2f} K
Rotational Speed : {machine["Rotational speed [rpm]"]} RPM
Torque : {machine["Torque [Nm]"]:.2f} Nm
Tool Wear : {machine["Tool wear [min]"]} Minutes

Machine Failure : {machine["Machine failure"]}

Tool Wear Failure : {machine["TWF"]}
Heat Dissipation Failure : {machine["HDF"]}
Power Failure : {machine["PWF"]}
Overstrain Failure : {machine["OSF"]}
Random Failure : {machine["RNF"]}

==================================================
ENGINEERING ANALYSIS
==================================================

Health Score : {eng["health_score"]}/100

Risk Level : {eng["risk"]}

Maintenance Priority : {eng["priority"]}

Estimated Mechanical Power : {eng["estimated_power"]:.2f} kW

Temperature Difference : {eng["delta_temperature"]:.2f} K

Tool Condition : {eng["tool_condition"]}

Thermal Status : {eng["thermal_status"]}

Remaining Useful Life : {eng["remaining_life"]} Hours

==================================================
INSTRUCTIONS
==================================================

Generate a professional predictive maintenance report for a facility maintenance engineer.

Use the following sections in this exact order.

## Machine Status

Explain the overall operating condition of the machine in 2–3 detailed paragraphs.

Describe how the current operating parameters indicate the machine's condition.

--------------------------------------------------

## Risk Status

Assess the current operational risk.

Explain why the machine is categorized as Low, Medium, High or Critical risk by considering:

- Health Score
- Failure Flags
- Thermal Status
- Tool Wear
- Estimated Mechanical Power

--------------------------------------------------

## Maintenance Report

Provide a detailed engineering assessment explaining:

- Overall machine performance
- Thermal behavior
- Mechanical loading
- Tool condition
- Remaining useful life
- Any abnormal operating trends

Do not simply repeat sensor values.

Explain their engineering significance.

--------------------------------------------------

## Recommendations

Provide 5–7 practical maintenance recommendations as bullet points suitable for a maintenance technician.

--------------------------------------------------

## Priority

State the maintenance priority (Low, Medium, High or Immediate).

Explain why this priority level has been assigned.

Mention whether maintenance is:

- Preventive
- Predictive
- Corrective

--------------------------------------------------

## Next Inspection

Recommend the next inspection interval and explain:

- When it should be performed
- What components should be inspected
- Which operating parameters should be monitored

--------------------------------------------------

## Conclusion

Write a detailed conclusion summarizing:

- Current machine condition
- Reliability
- Production impact
- Maintenance urgency
- Expected future performance if recommendations are followed.

==================================================
RULES
==================================================

1. Use professional industrial engineering language.
2. Do not repeat sensor values unnecessarily.
3. Explain engineering reasoning rather than only giving conclusions.
4. Keep each section concise and informative.
5. Recommendations must be bullet points.
6. Return clean Markdown.
7. Do not use tables.
8. Do not invent sensor values that are not provided.
9. Base the analysis only on the supplied engineering data.
10. Make the report suitable for an enterprise Facility Operations platform.
"""

        # --------------------------------------------------
        # Gemini Report
        # --------------------------------------------------

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        report = response.text.strip()

        # --------------------------------------------------
        # Work Order Generation
        # --------------------------------------------------

        if eng["risk"] == "Low":

            maintenance_type = "Preventive"
            estimated_time = "1 Hour"

        elif eng["risk"] == "Medium":

            maintenance_type = "Predictive"
            estimated_time = "2 Hours"

        elif eng["risk"] == "High":

            maintenance_type = "Corrective"
            estimated_time = "4 Hours"

        else:

            maintenance_type = "Emergency"
            estimated_time = "8 Hours"

        ai_summary = (
            f"TECHNICAL AUDIT: Machine {machine['Product ID']} shows {eng['risk']} risk status. "
            f"Health Score is {eng['health_score']}/100. "
            f"Observations: {eng['tool_condition']} tool condition and {eng['thermal_status']} thermal stability. "
            f"Estimated mechanical power output is {eng['estimated_power']} kW."
        )

        # --------------------------------------------------
        # Work Order Dictionary
        # --------------------------------------------------

        workorder = {

            "machine_id": machine["Product ID"],
            "machine_type": machine["Type"],
            "priority": eng["priority"],
            "maintenance_type": maintenance_type,
            "technician":"",
            "status": "Open",
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "estimated_cost": eng["maintenance_cost"],
            "estimated_time": estimated_time,
            "description": ai_summary

        }

        # --------------------------------------------------
        # Return Result
        # --------------------------------------------------

        return {

            "success": True,

            "report": report,

            "workorder": workorder

        }

    except Exception as e:

        return {

            "success": False,

            "report": f"""
# AI Maintenance Report

Unable to generate the maintenance report.

Error:
{str(e)}

Please verify:

- Gemini API Key
- Internet Connection
- Gemini Model Availability
""",

            "workorder": None

        }

def generate_preventive_recommendation(machine):

    prompt = f"""
You are a Senior Predictive Maintenance Engineer working in a smart manufacturing facility.

Analyze the following machine sensor data and generate a professional preventive maintenance recommendation.

Machine Information

Machine ID: {machine['Product ID']}
Machine Type: {machine['Type']}

Sensor Readings

Air Temperature : {machine['Air temperature [K]']} K
Process Temperature : {machine['Process temperature [K]']} K
Rotational Speed : {machine['Rotational speed [rpm]']} RPM
Torque : {machine['Torque [Nm]']} Nm
Tool Wear : {machine['Tool wear [min]']} minutes

Failure Information

Machine Failure : {"Yes" if machine["Machine failure"] else "No"}
Tool Wear Failure : {"Yes" if machine["TWF"] else "No"}
Heat Dissipation Failure : {"Yes" if machine["HDF"] else "No"}
Power Failure : {"Yes" if machine["PWF"] else "No"}
Overstrain Failure : {"Yes" if machine["OSF"] else "No"}
Random Failure : {"Yes" if machine["RNF"] else "No"}

Instructions

Use all available sensor values to assess the machine.

Do not simply repeat the sensor values.

Infer the machine condition from the readings.

Mention why the machine is healthy or risky.

Suggest preventive maintenance activities.

Estimate maintenance urgency.

Estimate downtime.

Suggest the next maintenance interval.

Keep the report concise and professional.

Return the response in the following format only.



WORK ORDER DESCRIPTION

Write only the maintenance work order description in 2–3 sentences (maximum 60 words).

The description should be suitable for directly storing in a maintenance work order.

Do not use headings, bullet points, markdown, or numbering inside the description.



AI PREVENTIVE MAINTENANCE RECOMMENDATION

## Machine Health

Explain the overall health of the machine.

## Risk Level

Mention the risk level and justify it.

## Maintenance Priority

Mention the maintenance priority and explain why.

## Recommended Maintenance Actions

- Action 1
- Action 2
- Action 3
- Action 4

## Components to Inspect

- Component 1
- Component 2
- Component 3

## Estimated Downtime

Provide the estimated maintenance duration.

## Recommended Next Maintenance

Mention the recommended maintenance interval.

## Summary

Provide a concise summary of the recommendation.



Rules

1. The Work Order Description must contain only plain text.
2. The AI Preventive Maintenance Recommendation must use exactly the headings shown above.
3. Keep the response concise, professional, and suitable for a facility maintenance engineer.
4. Do not include any additional sections or explanations.
5. Return clean Markdown.

"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    text = response.text

    parts = text.split("AI PREVENTIVE MAINTENANCE RECOMMENDATION")

    description = parts[0]
    description = description.replace("WORK ORDER DESCRIPTION", "").strip()

    recommendation = "AI PREVENTIVE MAINTENANCE RECOMMENDATION\n\n" + parts[1].strip()

    return {
        "description" : description,
        "recommendation" : recommendation
    }

def get_technical_summary(machine):
    """Generates a professional narrative technical description."""
    eng = engineering_summary(machine)
    
    # 1. Start with the general health status
    if machine['Machine failure'] == 1:
        status_part = f"The machine {machine['Product ID']} has experienced a critical failure and requires immediate intervention."
    else:
        status_part = f"The machine {machine['Product ID']} is currently operational with a health score of {eng['health_score']}/100."

    # 2. Add Thermal details
    thermal_part = f"Thermal analysis indicates a process temperature of {machine['Process temperature [K]']} K, which represents a {eng['thermal_status'].lower()} temperature delta of {eng['delta_temperature']} K relative to the air temperature."

    # 3. Add Mechanical details
    mechanical_part = f"Mechanical performance is currently maintained at {machine['Rotational speed [rpm]']} RPM with a torque load of {machine['Torque [Nm]']} Nm."

    # 4. Add Tool Wear details
    wear_part = f"The cutting tool has accumulated {machine['Tool wear [min]']} minutes of wear, placing it in the {eng['tool_condition'].lower()} category."

    # 5. Add Risk/Conclusion
    if eng['risk'] == "Low":
        conclusion = "Based on current sensor data, the operational risk is low, and routine monitoring is advised."
    else:
        conclusion = f"Due to the observed parameters, the machine is classified as {eng['risk']} risk, and {eng['priority'].lower()} priority maintenance is recommended."

    # Combine into a single paragraph of full sentences
    full_description = f"{status_part} {thermal_part} {mechanical_part} {wear_part} {conclusion}"
    
    return full_description