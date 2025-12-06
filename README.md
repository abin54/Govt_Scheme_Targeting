# 🏛️ Smart Government Scheme Targeting Tool

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![ML](https://img.shields.io/badge/ML-Clustering-orange.svg)
![Dashboard](https://img.shields.io/badge/Dashboard-Streamlit-red.svg)
![Policy](https://img.shields.io/badge/Domain-Public%20Policy-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A data-driven decision support system to prioritize districts for central/state welfare schemes using **composite need/risk scores** and clustering analysis. Designed for Indian public policy and governance.

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Data Sources](#-data-sources)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Scheme Scoring](#-scheme-scoring)
- [Dashboard Features](#-dashboard-features)
- [Author](#-author)

---

## 🎯 Overview

Government welfare schemes often struggle with **equitable resource allocation**. This tool addresses:

- ✅ **Multi-dimensional need assessment** across 20+ indicators
- ✅ **Scheme-specific prioritization** (Health, Education, PM-KISAN, Infrastructure)
- ✅ **District clustering** by development level
- ✅ **Budget allocation simulation**
- ✅ **Interactive policy dashboard**

### 💼 Impact Potential
| Metric | Value |
|--------|-------|
| Districts Analyzed | **700+** |
| Indicators Used | **20+** |
| Schemes Supported | **4** |

---

## ✨ Key Features

### 📊 Composite Need Scoring
Weighted indicators for each scheme type:

**Health Scheme:**
| Indicator | Weight |
|-----------|--------|
| Infant Mortality Rate | +25% |
| Maternal Mortality | +20% |
| Stunting Rate | +20% |
| Immunization Coverage | -15% |
| Sanitation | -10% |

**Education Scheme:**
| Indicator | Weight |
|-----------|--------|
| Literacy Rate | -25% |
| Female Literacy | -25% |
| Dropout Rate | +20% |
| Schools per Lakh | -15% |

### 🎯 District Clustering
- K-Means clustering (5 development categories)
- Very Low → Very High Development
- State-wise and national comparisons

### 💰 Budget Allocation Simulation
- Proportional to need score
- Per-capita weighted
- Equal distribution (top 50%)

---

## 📂 Data Sources

| Source | Indicators |
|--------|------------|
| **Census India** | Population, Literacy, Gender ratio |
| **NFHS** | IMR, MMR, Stunting, Immunization |
| **Agricultural Stats** | Crop yield, Irrigation |
| **PMGSY** | Road density |
| **RBI** | Bank branches, Per capita income |

*Note: Project includes synthetic data generator mimicking real patterns*

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Data Processing** | Pandas, NumPy |
| **Machine Learning** | Scikit-learn (K-Means) |
| **Geospatial** | GeoPandas, Folium |
| **Dashboard** | Streamlit, Plotly |

---

## 📁 Project Structure

```
03_Govt_Scheme_Targeting/
│
├── 📂 data/
│   ├── district_indicators.csv       # Raw indicators
│   └── district_scores.csv           # Computed scores
│
├── 📂 src/
│   ├── data_generator.py             # Synthetic data generator
│   ├── scoring_engine.py             # Need score calculation
│   └── clustering.py                 # District clustering
│
├── 📂 dashboard/
│   └── app.py                        # Policy simulation dashboard
│
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

```bash
git clone https://github.com/Abin544/govt-scheme-targeting.git
cd govt-scheme-targeting
pip install -r requirements.txt
```

---

## 📖 Usage

```bash
# Generate district data
cd src
python data_generator.py

# Calculate scores
python scoring_engine.py

# Launch dashboard
cd ../dashboard
streamlit run app.py
```

---

## 📊 Scheme Scoring

### Sample Priority Rankings (Health Scheme)

| Rank | District | State | Need Score |
|------|----------|-------|------------|
| 1 | Araria | Bihar | 89.3 |
| 2 | Purnia | Bihar | 87.1 |
| 3 | Kalahandi | Odisha | 85.7 |
| 4 | Shravasti | UP | 84.2 |
| 5 | Bahraich | UP | 83.8 |

---

## 🖥️ Dashboard Features

| Tab | Features |
|-----|----------|
| **Overview** | Development distribution, correlations |
| **Prioritization** | Scheme selection, top-N districts |
| **Budget Simulator** | Allocation methods, impact visualization |
| **State Analysis** | State vs national comparison, radar charts |

---

## 🔮 Future Enhancements

- [ ] Real-time data integration
- [ ] Geographic visualization (choropleth)
- [ ] Multi-objective optimization
- [ ] Impact prediction models
- [ ] API for government portals

---

## 👤 Author

**Shiva Krupa Abinash Sahu**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/shiva-krupa-abinash-sahu-211692193/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat&logo=github)](https://github.com/Abin544)

---

⭐ **Star this repo if you found it helpful!**
