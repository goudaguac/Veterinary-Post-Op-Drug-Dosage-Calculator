# app.py

import streamlit as st
from drug_data import DRUGS
import pandas as pd

st.set_page_config(page_title="Vet Dosage Calculator", page_icon="🐾")

st.title("🐾 Post-Op Veterinary Drug Dosage Calculator")
st.markdown(
    "Calculate immediate **post-operative dosages** for injectables and oral meds. "
    "Always confirm with a licensed veterinarian. "
)

# User inputs
species = st.radio("Animal species:", ["Dog", "Cat"])
weight = st.number_input("Patient weight (kg):", min_value=0.1, step=0.1)
drug = st.selectbox("Select a drug:", list(DRUGS.keys()))

# Dose calculation
if weight > 0 and drug:
    drug_info = DRUGS[drug]
    dose_per_kg = drug_info[species]["dose"]
    total_dose_mg = round(dose_per_kg * weight, 2)
    concentration = drug_info["concentration"]
    route = drug_info["route"]
    notes = drug_info["notes"]

    # Convert to mL if injectable
    if route == "Injectable":
        volume_ml = round(total_dose_mg / concentration, 2)
        st.success(
            f"{drug} dosage for a {weight} kg {species}: {total_dose_mg} mg "
            f"({volume_ml} mL at {concentration} mg/mL)"
        )
    else:
        st.success(
            f"{drug} dosage for a {weight} kg {species}: {total_dose_mg} mg (oral)"
        )

    st.markdown(f"**Route:** {route}")
    st.markdown(f"**Note:** {notes}")

st.markdown("---")
st.header("📚 Example Patient Records")

# Fake patient history (could be stored in a database later)
history_data = [
    {
        "Name": "Buddy",
        "Species": "Dog",
        "Weight (kg)": 12.0,
        "Drug": "Meloxicam",
        "Dose (mg)": 2.4,  # 0.2 mg/kg * 12kg
        "Volume (mL)": 0.48,  # assuming 5 mg/mL
        "Notes": "Injectable. Do not use with other NSAIDs."
    },
    {
        "Name": "Mittens",
        "Species": "Cat",
        "Weight (kg)": 4.5,
        "Drug": "Gabapentin",
        "Dose (mg)": 33.75,  # 7.5 mg/kg * 4.5kg
        "Volume (mL)": 0.68,  # assuming 50 mg/mL
        "Notes": "Oral. May cause sedation."
    },
    {
        "Name": "Max",
        "Species": "Dog",
        "Weight (kg)": 20.0,
        "Drug": "Cephalexin",
        "Dose (mg)": 500.0,  # 25 mg/kg * 20kg
        "Volume (mL)": 2.0,  # assuming 250 mg/mL
        "Notes": "Oral. Check for penicillin allergies."
    },
    {
        "Name": "Whiskers",
        "Species": "Cat",
        "Weight (kg)": 3.0,
        "Drug": "Bupivacaine",
        "Dose (mg)": 4.5,  # 1.5 mg/kg * 3kg
        "Volume (mL)": 0.9,  # assuming 5 mg/mL
        "Notes": "Injectable local anesthetic."
    },
    {
        "Name": "Rocky",
        "Species": "Dog",
        "Weight (kg)": 25.0,
        "Drug": "Buprenorphine",
        "Dose (mg)": 0.38,  # 0.015 mg/kg * 25kg
        "Volume (mL)": 1.27,  # assuming 0.3 mg/mL
        "Notes": "Injectable opioid."
    },
]

df_history = pd.DataFrame(history_data)
st.dataframe(df_history)


