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
            {"Date": today, "Name": "Shadow", "Species": "Cat", "Weight": 4.2}}

