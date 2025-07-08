# app.py

import streamlit as st
import pandas as pd
from datetime import datetime

# ------------------------
# Example data
# ------------------------
DRUGS = {
    "Meloxicam": {
        "Dog": 0.2, "Cat": 0.05, "Bird": 0.1, "Unit": "mg/kg",
        "Route": "Injectable or oral",
        "Note": "Do NOT use with other NSAIDs. Use lowest effective dose.",
        "Concentration": 5
    },
    "Gabapentin": {
        "Dog": 15, "Cat": 7.5, "Bird": 10, "Unit": "mg/kg",
        "Route": "Oral only",
        "Note": "Sedation may occur. Best given on empty stomach.",
        "Concentration": 50
    },
}

VET_TECHS = ["Alex Tan", "Jamie Lee", "Morgan Smith"]
VETS = ["Dr. Wong", "Dr. Patel", "Dr. Fernandez"]

# ------------------------
# Layout
# ------------------------
st.set_page_config(layout="wide")

st.title("🐾 Vet Post-Op Drug Dosage Calculator")

left, right = st.columns(2)

with left:
    st.header("📋 Patient & Calculation")

    # Patient name
    patient_name = st.text_input("Patient Name:", "")

    # Species selector: rectangles
    st.markdown("### Species:")
    species_col1, species_col2, species_col3, species_col4 = st.columns(4)
    species = st.session_state.get("species", None)

    with species_col1:
        if st.button("🐶 Dog"):
            species = "Dog"
    with species_col2:
        if st.button("🐱 Cat"):
            species = "Cat"
    with species_col3:
        if st.button("🐦 Bird"):
            species = "Bird"
    with species_col4:
        if st.button("🦎 Other"):
            species = "Other"

    if species == "Other":
        species = st.text_input("Enter species:", "")

    st.session_state["species"] = species

    # Operation
    operation = st.text_input("Operation:", placeholder="e.g. Neuter, Dental, Lump removal")

    # Vet tech & vet
    vet_tech = st.selectbox("Vet Tech in charge:", VET_TECHS)
    veterinarian = st.selectbox("Supervising Veterinarian:", VETS)

    # Weight
    weight = st.number_input("Patient weight (kg):", min_value=0.1, step=0.1)

    # Drug
    drug = st.selectbox("Select Drug:", list(DRUGS.keys()))
    conc = st.number_input(f"Drug concentration (mg/mL):", value=float(DRUGS[drug]["Concentration"]), step=0.1)

    # Calculate
    if all([patient_name, species, weight > 0]):
        dose_per_kg = DRUGS[drug].get(species, DRUGS[drug]["Dog"])
        total_mg = round(dose_per_kg * weight, 2)
        total_ml = round(total_mg / conc, 2)

        # Big colorful output
        st.markdown(f"""
        <div style="border: 2px solid #4CAF50; padding: 10px; background-color: #F0FFF0;">
        <h3 style="color:#2E8B57;">💉 Dosage:</h3>
        <p style="font-size:28px; font-weight:bold;">{total_mg} mg</p>
        <h3 style="color:#2E8B57;">📏 Volume to Draw:</h3>
        <p style="font-size:28px; font-weight:bold;">{total_ml} mL</p>
        </div>
        """, unsafe_allow_html=True)

        # Route & Note
        st.markdown(f"""
        <div style="border: 1px solid #2196F3; padding: 10px; background-color: #E3F2FD;">
        <b>Route:</b> {DRUGS[drug]["Route"]}  
        <br><b>Note:</b> {DRUGS[drug]["Note"]}
        </div>
        """, unsafe_allow_html=True)

    else:
        st.info("✅ Enter name, species, weight to calculate dose.")


with right:
    st.header("📚 Patient Records (Editable)")

    # Example patient log
    if "patient_data" not in st.session_state:
        st.session_state["patient_data"] = pd.DataFrame([
            {"Date": datetime.today().strftime("%Y-%m-%d"), "Name": "Bella", "Species": "Dog", "Weight": 10.2, 
             "Drug": "Meloxicam", "Dose_mg": 2.04, "Volume_mL": 0.4, "Vet_Tech": "Jamie Lee", "Vet": "Dr. Wong", "Operation": "Spay"},
            {"Date": datetime.today().strftime("%Y-%m-%d"), "Name": "Mochi", "Species": "", "Weight": 3.4, 
             "Drug": "Gabapentin", "Dose_mg": 25.5, "Volume_mL": 0.5, "Vet_Tech": "", "Vet": "", "Operation": ""}
        ])

    edited_df = st.data_editor(
        st.session_state["patient_data"],
        num_rows="dynamic",
        use_container_width=True
    )

    st.session_state["patient_data"] = edited_df

    st.write("✅ Records are editable for missing fields and auto-date stamped.")


df_history = pd.DataFrame(history_data)
st.dataframe(df_history)


