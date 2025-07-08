# drug_data.py

DRUGS = {
    "Meloxicam": {
        "Dog": {"dose": 0.2},
        "Cat": {"dose": 0.05},
        "concentration": 5,  # mg/mL (injectable)
        "route": "Injectable",
        "notes": "Do not combine with other NSAIDs. Injectable form for immediate post-op use."
    },
    "Gabapentin": {
        "Dog": {"dose": 15},
        "Cat": {"dose": 7.5},
        "concentration": 50,  # mg/mL (oral suspension)
        "route": "Oral",
        "notes": "Oral only. May cause sedation. Use to calm patients before transport."
    },
    "Cephalexin": {
        "Dog": {"dose": 25},
        "Cat": {"dose": 25},
        "concentration": 250,  # mg/mL (oral suspension)
        "route": "Oral",
        "notes": "Oral antibiotic. Check for penicillin allergies."
    },
    "Bupivacaine": {
        "Dog": {"dose": 1.5},
        "Cat": {"dose": 1.5},
        "concentration": 5,  # mg/mL (injectable)
        "route": "Injectable",
        "notes": "Injectable local anesthetic. Do not exceed safe total dose."
    },
    "Buprenorphine": {
        "Dog": {"dose": 0.015},
        "Cat": {"dose": 0.015},
        "concentration": 0.3,  # mg/mL (injectable)
        "route": "Injectable",
        "notes": "Injectable opioid analgesic. For immediate post-op pain relief."
    }
}
