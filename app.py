# app.py

import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import json

# -----------------------------
# Streamlit config
# -----------------------------
st.set_page_config(page_title="Vet Post-Op Drug Dosage Calculator", layout="wide")
st.title("🐾 Vet Post-Op Drug Dosage Calculator")

# -----------------------------
# Google Sheets connector
# -----------------------------
def get_gsheet_client():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    if "google_service_account" in st.secrets:
        service_account_info = dict(st.secrets["google_service_account"])
        creds = Credentials.from_service_account_info(
            service_account_info, scopes=scopes
        )
    else:
        creds = Credentials.from_service_account_file(
            "service_account.json",
            scopes=scopes
        )

    client = gspread.authorize(creds)
    return client


def get_worksheet(sheet_name, worksheet_name):
    client = get_gsheet_client()
    sheet = client.open(sheet_name)
    worksheet = sheet.worksheet(worksheet_name)
    return worksheet

def load_vet_records(vet_name):
    worksheet = get_worksheet("Vet_Drug_Records", vet_name)
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

def save_vet_records(vet_name, df):
    worksheet = get_worksheet("Vet_Drug_Records", vet_name)
    worksheet.clear()
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

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

    if all([patient_name, species, weight > 0]):
        dose_per_kg = DRUGS[drug].get(species, DRUGS[drug]["Dog"])
        total_mg = round(dose_per_kg * weight, 2)
        total_ml = round(total_mg / conc, 2)

        st.markdown(f"""
        <div style="border: 2px solid #4CAF50; padding: 10px; background-color: #F0FFF0;">
        <h3 style="color:#2E8B57;">💉 Dosage:</h3>
        <p style="font-size:28px; font-weight:bold;">{total_mg} mg</p>
        <h3 style="color:#2E8B57;">📏 Volume to Draw:</h3>
        <p style="font-size:28px; font-weight:bold;">{total_ml} mL</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="border: 1px solid #2196F3; padding: 10px; background-color: #E3F2FD;">
        <b>Route:</b> {DRUGS[drug]["Route"]}<br>
        <b>Note:</b> {DRUGS[drug]["Note"]}
        </div>
        """, unsafe_allow_html=True)

        if st.button("💾 Save to Records"):
            new_row = {
                "Date": datetime.today().strftime("%Y-%m-%d"),
                "Name": patient_name,
                "Species": species,
                "Weight": weight,
                "Drug": drug,
                "Dose_mg": total_mg,
                "Volume_mL": total_ml,
                "Vet_Tech": vet_tech,
                "Vet": veterinarian,
                "Operation": operation
            }
            df_existing = load_vet_records(veterinarian)
            df_updated = pd.concat([df_existing, pd.DataFrame([new_row])], ignore_index=True)
            save_vet_records(veterinarian, df_updated)
            st.success(f"Record saved to {veterinarian}'s worksheet!")

    else:
        st.info("✅ Enter name, species, weight to calculate.")

with right:
    st.header("📚 Patient Records (by Vet)")
    for vet in VETS:
        st.subheader(f"👨‍⚕️ {vet}")
        df_vet = load_vet_records(vet)
        edited_df = st.data_editor(df_vet, num_rows="dynamic", use_container_width=True, key=vet)
        if st.button(f"💾 Save {vet} Records"):
            save_vet_records(vet, edited_df)
            st.success(f"{vet}'s records updated!")

