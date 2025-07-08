# app.py

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Vet Post-Op Drug Dosage Calculator", layout="wide")
st.title("🐾 Vet Post-Op Drug Dosage Calculator")

# -----------------------------
# Example drugs
# -----------------------------
DRUGS = {
    "Meloxicam": {
        "Dog": 0.2, "Cat": 0.05, "Bird": 0.1, "Unit": "mg/kg",
        "Route": "Injectable or oral",
        "Note": "Do NOT use with other NSAIDs.",
        "Concentration": 5
    },
    "Gabapentin": {
        "Dog": 15, "Cat": 7.5, "Bird": 10, "Unit": "mg/kg",
        "Route": "Oral only",
        "Note": "Sedation may occur.",
        "Concentration": 50
    },
}

VET_TECHS = ["Alex Tan", "Jamie Lee", "Morgan Smith"]
VETS = ["Dr. Wong", "Dr. Patel", "Dr. Fernandez"]

# -----------------------------
# Fake patient records store
# -----------------------------
@st.cache_data
def get_fake_records():
    today = datetime.today().strftime("%Y-%m-%d")
    data = {
        "Dr. Wong": pd.DataFrame([
            {"Date": today, "Name": "Bella", "Species": "Dog", "Weight": 12.5,
             "Drug": "Meloxicam", "Dose_mg": 2.5, "Volume_mL": 0.5, "Vet_Tech": "Alex Tan",
             "Operation": "Spay"},
            {"Date": today, "Name": "Shadow", "Species": "Cat", "Weight": 4.2,
             "Drug": "Gabapentin", "Dose_mg": 31.5, "Volume_mL": 0.63, "Vet_Tech": "Jamie Lee",
             "Operation": "Dental"}
        ]),
        "Dr. Patel": pd.DataFrame([
            {"Date": today, "Name": "Luna", "Species": "Bird", "Weight": 0.3,
             "Drug": "Meloxicam", "Dose_mg": 0.03, "Volume_mL": 0.01, "Vet_Tech": "Morgan Smith",
             "Operation": "Wing Repair"},
            {"Date": today, "Name": "Ollie", "Species": "Dog", "Weight": 18.0,
             "Drug": "Gabapentin", "Dose_mg": 270, "Volume_mL": 5.4, "Vet_Tech": "",
             "Operation": ""}
        ]),
        "Dr. Fernandez": pd.DataFrame([
            {"Date": today, "Name": "Coco", "Species": "Cat", "Weight": 5.1,
             "Drug": "Meloxicam", "Dose_mg": 0.25, "Volume_mL": 0.05, "Vet_Tech": "Jamie Lee",
             "Operation": "Lumpectomy"},
            {"Date": today, "Name": "Max", "Species": "", "Weight": "",
             "Drug": "", "Dose_mg": "", "Volume_mL": "", "Vet_Tech": "", "Operation": ""}
        ])
    }
    return data

fake_records = get_fake_records()

# -----------------------------
# Layout
# -----------------------------
left, right = st.columns(2)

with left:
    st.header("📋 Patient & Dosage")

    patient_name = st.text_input("Patient Name:", "")
    st.markdown("### Species:")
    col1, col2, col3, col4 = st.columns(4)
    species = st.session_state.get("species", None)
    with col1:
        if st.button("🐶 Dog"):
            species = "Dog"
    with col2:
        if st.button("🐱 Cat"):
            species = "Cat"
    with col3:
        if st.button("🐦 Bird"):
            species = "Bird"
    with col4:
        if st.button("🦎 Other"):
            species = "Other"

    if species == "Other":
        species = st.text_input("Enter species:")

    st.session_state["species"] = species

    operation = st.text_input("Operation:", placeholder="e.g. Neuter, Dental, Lump removal")
    vet_tech = st.selectbox("Vet Tech in charge:", VET_TECHS)
    veterinarian = st.selectbox("Supervising Veterinarian:", VETS)
    weight = st.number_input("Patient weight (kg):", min_value=0.1, step=0.1)
    drug = st.selectbox("Select Drug:", list(DRUGS.keys()))
    conc = st.number_input(f"Drug concentration (mg/mL):", value=float(DRUGS[drug]["Concentration"]), step=0.1)

with right:
    st.markdown("## 💉 Calculation")
    if all([patient_name, species, weight > 0]):
        dose_per_kg = DRUGS[drug].get(species, DRUGS[drug]["Dog"])
        total_mg = round(dose_per_kg * weight, 2)
        total_ml = round(total_mg / conc, 2)

        st.markdown(f"""
        <div style="border: 2px solid #4CAF50; padding: 10px; background-color: #F0FFF0;">
        <h4 style="color:#2E8B57;">Dosage:</h4>
        <p style="font-size:24px; font-weight:bold;">{total_mg} mg</p>
        <h4 style="color:#2E8B57;">Volume:</h4>
        <p style="font-size:24px; font-weight:bold;">{total_ml} mL</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="border: 1px solid #2196F3; padding: 10px; background-color: #E3F2FD;">
        <b>Route:</b> {DRUGS[drug]["Route"]}<br>
        <b>Note:</b> {DRUGS[drug]["Note"]}
        </div>
        """, unsafe_allow_html=True)

    else:
        st.info("✅ Enter name, species, weight to calculate.")

# Add space below the calculation bubbles
with right:
    st.markdown("---")
    st.header("📚 Example Patient Records")
    for vet in VETS:
        st.subheader(f"👨‍⚕️ {vet}")
        df_vet = fake_records[vet]
        st.dataframe(df_vet, use_container_width=True)
