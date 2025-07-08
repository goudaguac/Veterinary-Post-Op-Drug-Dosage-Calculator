
# 🐾 Vet Tech Post-Op Drug Dosage Calculator

This **Streamlit app** helps veterinary technicians calculate **immediate post-operative drug dosages** for dogs and cats.  
It supports common injectables and oral medications, and includes example patient records for quick reference.

---

## 🚀 Features

- ✅ Calculates drug dosages based on species and weight
- ✅ Converts from mg to mL based on drug concentration (for injectables)
- ✅ Shows administration route (Injectable or Oral)
- ✅ Displays important drug-specific notes and warnings
- ✅ Includes a simple **history table** with example patients for easy reference

---

## 💉 Included Drugs (Demo)

| Drug         | Route       | Notes                                      |
|--------------|-------------|--------------------------------------------|
| Meloxicam    | Injectable  | NSAID, do not combine with other NSAIDs   |
| Gabapentin   | Oral        | Sedation possible, for pain management    |
| Cephalexin   | Oral        | Antibiotic, check for penicillin allergy  |
| Bupivacaine  | Injectable  | Local anesthetic, use carefully           |
| Buprenorphine| Injectable  | Opioid analgesic                          |

> 📌 **Disclaimer:** Dosages are indicative only. Always verify with a licensed veterinarian.

---

## 📚 Example Patient History

The app includes a fake **patient record table** with sample animals (name, species, weight, drug, dose in mg & mL, and notes)  
This demonstrates how vet techs might refer back to previous calculations.

---

## 🏃‍♀️ How to Run Locally

1. **Clone the repo:**

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name

2. **Install dependencies**
   
 ```pip install -r requirements.txt

3. **Run the app**

```streamlit run app.py


