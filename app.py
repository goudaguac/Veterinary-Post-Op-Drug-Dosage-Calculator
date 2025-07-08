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
    # Load from Streamlit secrets
    service_account_info = json.loads(
        st.secrets["google_service_account"].to_json()
    )
    creds = Credentials.from_service_account_info(
        service_account_info, scopes=scopes
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



