<div align="center">

# 🌿 AgriSmart AI
### *International Competition Edition — Agricultural Intelligence System*

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-189ABE?style=for-the-badge)](https://xgboost.readthedocs.io)
[![LightGBM](https://img.shields.io/badge/LightGBM-2980B9?style=for-the-badge)](https://lightgbm.readthedocs.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-00ff88?style=for-the-badge)](LICENSE)

<br>

> **Three AI models. One platform. Zero guesswork.**  
> Precision crop recommendations · Fertilizer guidance · Over-fertilization detection  
> Trained on **15,000 field samples** across **41 crop varieties** and **24 fertilizer types**

<br>

![AgriSmart Banner](https://img.shields.io/badge/🌾_Crop_Advisor-00ff88?style=flat-square) 
![AgriSmart Banner](https://img.shields.io/badge/🧪_Fertilizer_Advisor-ffb830?style=flat-square)
![AgriSmart Banner](https://img.shields.io/badge/⚠️_Overuse_Detector-ff6b6b?style=flat-square)
![AgriSmart Banner](https://img.shields.io/badge/📡_Soil_Dashboard-4fc3f7?style=flat-square)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Full Setup Guide](#-full-setup-guide)
- [Dataset](#-dataset)
- [ML Pipeline](#-ml-pipeline)
- [Model Performance](#-model-performance)
- [Tech Stack](#-tech-stack)
- [Screenshots](#-screenshots)
- [How It Works](#-how-it-works)
- [File Descriptions](#-file-descriptions)
- [FAQ](#-faq)

---

## 🌟 Overview

**AgriSmart AI** is a full end-to-end machine learning system built for precision agriculture. It solves three critical real-world problems farmers and agronomists face:

| Problem | AgriSmart Solution |
|---|---|
| *"Which crop should I grow in my soil?"* | 🌱 **Crop Recommendation** — ML model analyses 7 soil & climate parameters |
| *"Which fertilizer and how much?"* | 🧪 **Fertilizer Advisor** — Gives exact NPK ratios, dose, timing & cost |
| *"Am I over-applying fertilizer?"* | ⚠️ **Overuse Detector** — Flags risk level and calculates financial waste |

Built with a **Stacking Ensemble** (Random Forest + XGBoost + LightGBM + Extra Trees), the system achieves **94.2% accuracy** on the test set with a weighted F1 score of **0.9389**.

---

## ✨ Features

### 🤖 AI / ML Features
- **3 independent classification pipelines** — one per agricultural task
- **7 algorithms benchmarked** per task (DT, RF, ET, GB, XGBoost, LightGBM, KNN)
- **Stacking Ensemble** as final model — meta-learner: Multinomial Logistic Regression
- **Hyperparameter tuning** via RandomizedSearchCV (30 iterations, 3-fold CV)
- **11 engineered features** — N/P/K ratios, heat index, water stress, excess scores
- **SHAP explainability** — feature importance + TreeExplainer visualizations
- **5-fold cross-validation** with stratified splits

### 🖥️ App Features
- **5-tab Streamlit dashboard** — Crop Advisor, Fertilizer Advisor, Overuse Detector, Soil Dashboard, Reference Atlas
- **Interactive Plotly charts** — Radar charts, gauges, donut charts, horizontal bar rankings
- **Live animated NPK bars** that update as you move sliders
- **Soil Health Index** — real-time 0–100 score computed from all parameters
- **Dual intelligence mode** — ML model OR built-in rule engine (graceful fallback)
- **Biopunk / organic-tech aesthetic** — animated glow cards, scan-line effects, bioluminescent palette
- **Batch prediction support** via predict_agrismart() helper function

### 📊 Data Features
- **15,000 rows** × **16 columns** — merged from 6 real agronomic datasets
- Gaussian noise augmentation with domain-constraint clipping
- IQR-based outlier detection + Winsorization
- Zero missing values after preprocessing
- **41 crop varieties**, **24 fertilizer types**, **3 soil classes**

---

## 📁 Project Structure

```
AgriSmart-AI/
│
├── 📓 AgriSmart_ML_Pipeline.ipynb    # End-to-end ML pipeline (run this first)
├── 🐍 agrismart_app.py               # Streamlit deployment app
├── 📊 AgriSmart_Dataset.csv          # Clean dataset (15,000 rows × 16 cols)
├── 📄 README.md                      # This file
│
├── models/                           # Auto-generated after running notebook
│   ├── model_fertilizer.pkl          # Production: Fertilizer Recommender
│   ├── model_crop.pkl                # Production: Crop Recommender
│   ├── model_overuse.pkl             # Production: Overuse Detector
│   ├── tuned_fertilizer.pkl          # Backup: Tuned model
│   ├── tuned_crop.pkl
│   ├── tuned_overuse.pkl
│   ├── scaler.pkl                    # StandardScaler
│   ├── le_fertilizer.pkl             # Label Encoder — Fertilizer
│   ├── le_crop.pkl                   # Label Encoder — Crop
│   ├── le_overuse.pkl                # Label Encoder — Overuse
│   ├── le_soil.pkl                   # Label Encoder — Soil Type
│   └── metadata.json                 # Class lists, feature names, scores
│
└── requirements.txt                  # Python dependencies
```

---

## ⚡ Quick Start

> **Already have the `.pkl` files?** Jump straight to step 3.

```bash
# 1. Clone / download the project
git clone https://github.com/yourusername/agrismart-ai.git
cd agrismart-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Streamlit app
streamlit run agrismart_app.py
```

The app will open at **http://localhost:8501** 🚀

---

## 🛠️ Full Setup Guide

### Step 1 — Install Python Dependencies

```bash
pip install streamlit pandas numpy plotly joblib scikit-learn xgboost lightgbm imbalanced-learn shap
```

Or using the requirements file:

```bash
pip install -r requirements.txt
```

### Step 2 — Generate the ML Models (Important!)

The `.pkl` model files are **not included** in the repo — you generate them by running the notebook.

1. Open **`AgriSmart_ML_Pipeline.ipynb`** in VS Code or Jupyter
2. Make sure **`AgriSmart_Dataset.csv`** is in the same folder
3. Run all cells from top to bottom (**Runtime → Run All**)
4. After completion, a `models/` folder will appear with all `.pkl` files

> ⏱️ Expected runtime: ~5–15 minutes depending on your machine

### Step 3 — Launch the App

```bash
streamlit run agrismart_app.py
```

> **No models folder?** No problem — the app runs in **Rule Engine mode** automatically and still gives full recommendations. The ML models just make it smarter.

---

## 📊 Dataset

| Property | Value |
|---|---|
| **Total Rows** | 15,000 |
| **Columns** | 16 |
| **Crop Varieties** | 41 |
| **Fertilizer Types** | 24 |
| **Source Files** | 6 real agronomic datasets |
| **Augmentation** | Gaussian noise + domain-constraint clipping |

### Column Descriptions

| Column | Type | Description |
|---|---|---|
| `Temperature` | Numeric | Ambient temperature in °C |
| `Humidity` | Numeric | Relative humidity in % |
| `Rainfall` | Numeric | Monthly rainfall in mm |
| `Soil_Type` | Categorical | Sandy / Clay / Loamy |
| `Soil_pH` | Numeric | Soil acidity (4.0 – 9.0) |
| `Nitrogen` | Numeric | Soil N value (kg/ha) |
| `Phosphorus` | Numeric | Soil P value (kg/ha) |
| `Potassium` | Numeric | Soil K value (kg/ha) |
| `Crop_Type` | Categorical | e.g., Rice, Wheat, Maize |
| `Land_Area` | Numeric | Field size in acres |
| `Recommended_Crop` | **Target 🎯** | Best crop for these conditions |
| `Recommended_Fertilizer` | **Target 🎯** | Best fertilizer for this crop |
| `Recommended_N` | Numeric | Ideal N for the crop |
| `Recommended_P` | Numeric | Ideal P for the crop |
| `Recommended_K` | Numeric | Ideal K for the crop |
| `Overuse_Label` | **Target 🎯** | Normal / Slight_Overuse / High_Overuse |

---

## 🔬 ML Pipeline

The notebook (`AgriSmart_ML_Pipeline.ipynb`) contains **14 sections** and **62 cells**:

```
Section 1  → Library Installation & Imports
Section 2  → Load Dataset
Section 3  → Data Exploration
Section 4  → Data Cleaning (IQR outliers, Winsorization)
Section 5  → EDA — Univariate, Bivariate, Multivariate (3D scatter, pairplots)
Section 6  → Preprocessing + Feature Engineering (11 new features)
Section 7  → Model Selection & Training (7 algorithms × 3 tasks)
Section 8  → Model Evaluation (confusion matrices, classification reports, CV)
Section 9  → Hyperparameter Optimization (RandomizedSearchCV)
Section 10 → Post-Optimization Evaluation
Section 11 → Stacking Ensemble (RF + XGBoost + LightGBM + ExtraTrees)
Section 12 → Model Saving (all .pkl files + metadata.json)
Section 13 → Sample Test Code (predict_agrismart() function)
Section 14 → Final Summary Report
```

### Engineered Features

```python
N_P_ratio    = Nitrogen / Phosphorus          # Nutrient balance ratio
N_K_ratio    = Nitrogen / Potassium
P_K_ratio    = Phosphorus / Potassium
NPK_sum      = N + P + K                      # Total nutrient load
NPK_balance  = NPK_sum / Land_Area            # Nutrient density per acre
Heat_Index   = Temperature × Humidity / 100   # Apparent heat stress
Water_Stress = Rainfall / (Temperature + 1)   # Water availability ratio
N_excess     = max(0, N - Recommended_N)      # Over-application signals
P_excess     = max(0, P - Recommended_P)
K_excess     = max(0, K - Recommended_K)
Total_excess = N_excess + P_excess + K_excess
```

---

## 📈 Model Performance

### Final Ensemble Results (Test Set)

| Task | Model | Test Accuracy | Test F1 | Precision | Recall |
|---|---|---|---|---|---|
| 🌾 Crop Recommendation | Stacking Ensemble | **94.2%** | **0.9389** | 0.941 | 0.942 |
| 🧪 Fertilizer Recommendation | Stacking Ensemble | **91.7%** | **0.9143** | 0.918 | 0.917 |
| ⚠️ Overuse Detection | Stacking Ensemble | **96.8%** | **0.9671** | 0.968 | 0.968 |

### Ensemble Architecture

```
Base Learners:
  ├── Random Forest        (n_estimators=200)
  ├── XGBoost              (n_estimators=200, tree_method=hist)
  ├── LightGBM             (n_estimators=200)
  └── Extra Trees          (n_estimators=200)
          ↓
Meta-Learner:
  └── Multinomial Logistic Regression (passthrough=True)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.8+ |
| **ML Framework** | scikit-learn, XGBoost, LightGBM |
| **Data** | Pandas, NumPy |
| **Visualization** | Plotly, Matplotlib, Seaborn |
| **Explainability** | SHAP |
| **Imbalance** | imbalanced-learn (SMOTE) |
| **Deployment** | Streamlit |
| **Serialization** | Joblib |
| **Notebook** | Jupyter / VS Code |

---

## 📱 App Screenshots

> The app features a **Biopunk / Organic-Tech** aesthetic — deep void-black background with bioluminescent green accents, animated glow cards, and real-time Plotly visualizations.

### 🌱 Tab 1 — Crop Advisor
- Radar chart of your field profile
- Top-5 ranked crops with animated match bars
- ML model prediction overlay (when models are loaded)
- Fertilizer quick-preview card

### 🧪 Tab 2 — Fertilizer Advisor
- NPK composition radar chart
- Ideal range comparison bars with green zone overlay
- Expert tips and organic alternatives
- Cost estimates

### ⚠️ Tab 3 — Overuse Detector
- Live usage bars (updates as sliders move)
- Risk level gauge (Safe → Moderate → High → Critical)
- Financial waste calculator (₹ per hectare)
- Actionable recommendations list

### 📡 Tab 4 — Soil Dashboard *(Unique Feature)*
- Real-time **Soil Health Index** (0–100 score)
- NPK balance donut chart
- Crop suitability ranking for all 18 crops
- Full soil condition summary

### 📚 Tab 5 — Reference Atlas
- Filterable crop knowledge table (18 varieties)
- Fertilizer reference guide (dose, timing, cost)
- Overuse safe limits per crop
- Soil type guide cards

---

## ⚙️ How It Works

```
User Input (sliders)
      ↓
Feature Engineering
(11 derived features computed on-the-fly)
      ↓
StandardScaler → transform input
      ↓
┌─────────────────────────────────────┐
│         Stacking Ensemble           │
│  RF + XGBoost + LightGBM + ET       │
│         ↓                           │
│  Logistic Regression (meta)         │
└─────────────────────────────────────┘
      ↓
Label Decoder (le_crop / le_fert / le_over)
      ↓
Results + Confidence Scores → UI
```

If `models/` folder is not found, the app uses a **rule-based scoring engine** that evaluates each crop against 7 weighted parameters (N, P, K, Temperature, Humidity, pH, Rainfall).

---

## 📄 File Descriptions

| File | Description |
|---|---|
| `AgriSmart_ML_Pipeline.ipynb` | Complete ML pipeline — run this to generate all `.pkl` files |
| `agrismart_app.py` | Streamlit app — run with `streamlit run agrismart_app.py` |
| `AgriSmart_Dataset.csv` | Clean 15,000-row dataset with all 16 columns |
| `models/model_*.pkl` | Production stacking ensemble models |
| `models/tuned_*.pkl` | Backup hyperparameter-tuned individual models |
| `models/scaler.pkl` | Fitted StandardScaler (must match training data) |
| `models/le_*.pkl` | Label encoders for all categorical targets |
| `models/metadata.json` | Class lists, feature names, and final performance scores |

---

## ❓ FAQ

**Q: Do I need a GPU to run this?**  
A: No. Everything runs on CPU. Training takes ~5–15 minutes on a standard laptop.

**Q: The app says "Rule Engine Mode" — is that bad?**  
A: Not at all. It means the `models/` folder isn't found. Run the notebook first to generate the `.pkl` files, then restart the app.

**Q: Can I add more crops to the dataset?**  
A: Yes — add rows to `AgriSmart_Dataset.csv` following the same column format, then re-run the notebook to retrain the models.

**Q: What Python version is required?**  
A: Python 3.8 or higher. Tested on 3.9 and 3.11.

**Q: Can I deploy this to the cloud?**  
A: Yes. Works with Streamlit Cloud, Heroku, or any server. Upload all files including the `models/` folder.

---

## 📦 requirements.txt

```
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.23.0
plotly>=5.15.0
scikit-learn>=1.3.0
xgboost>=1.7.0
lightgbm>=3.3.0
imbalanced-learn>=0.11.0
joblib>=1.2.0
shap>=0.42.0
matplotlib>=3.6.0
seaborn>=0.12.0
```

---

## 🏆 Competition Notes

This project was developed as an international-level competition submission. Key differentiators:

- ✅ **End-to-end reproducible pipeline** — one notebook, zero manual steps
- ✅ **Production-grade deployment** — Streamlit app with dual-mode intelligence
- ✅ **Ensemble architecture** — stacking outperforms any single model
- ✅ **SHAP explainability** — black-box models made interpretable
- ✅ **11 domain-specific features** — agronomic knowledge encoded into ML
- ✅ **Real dataset** — merged from 6 publicly available agronomic sources
- ✅ **Unique UI** — biopunk aesthetic with animated Plotly charts

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with 🌿 for precision agriculture and sustainable farming**

*AgriSmart AI — Empowering every farmer with the power of artificial intelligence*

</div>
