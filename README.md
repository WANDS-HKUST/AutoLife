<p align="center">
  <img src="img/logo.png" alt="Project Logo" width="260" />
</p>

<h1 align="center">🚀 AutoLife Benchamrk: Automatic Life Journaling with Smartphones and LLMs</h1>

<p align="center">
  <a href="#" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python">
  </a>
  <a href="#" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  </a>
  <a href="https://github.com/WANDS-HKUST/AutoLife" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/github/stars/WANDS-HKUST/AutoLife?style=social&cacheSeconds=3600" alt="GitHub stars">
  </a>
  <a href="https://dl.acm.org/doi/10.1145/3680207.3765261" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/Paper-IMWUT%202025-ff69b4?logo=academia&logoColor=white" alt="IMWUT(Ubicomp) 2025 paper">
  </a>
</p>



---
# AutoLife
A multimodal **sensor dataset with aligned reference journals** capturing real-world user behaviors during daily activities (e.g., walking, studying, commuting) in a campus environment.  
The dataset supports research on **automatic life logging, behavior understanding, context modeling, and human-centered sensing systems**.

---

## 📌 Dataset Overview

Each record contains:
- 📱 **Smartphone sensor data** collected during real-world usage
- 📝 **Reference journals** describing user behaviors and activities
- ⏱️ **Temporal annotations** for behavior segments

Example scenarios include campus mobility, indoor stays, short transitions, and daily routines.

### Basic Statistics

| Metric | Value |
|--------|-------|
| Total duration | 370.02 hours |
| Mean segment duration | 2.20 hours |
| Median segment duration | 1.78 hours |

---

## 📥 Download Dataset

Dataset is available at:

👉 [Download here](https://drive.google.com/file/d/16hXedIOmaIZJ82wbdIaJIiGSw6bEF_PU/view?usp=sharing)

After downloading, unzip the dataset:

```bash
unzip autolife_dataset.zip -d data/
```
## ⚙️ Setup

We recommend Python 3.8+.

Install dependencies:
```bash
pip install -r requirements.txt
```

## 📂 Dataset Structure
``` text
data/
├── experiment/ //Raw sensor streams collected during the experiment
│   ├── accelerometer.csv // accelerometer sensor measurements with timestamps.
│   ├── gyroscope.csv
│   ├── location.csv
│   ├── wifi.csv
│   ├── label.csv // experiment start and end time
│   └── [other_sensor].csv
├── reference_journals.json // Reference journals describing user behaviors annotations.
└── metadata.csv // Dataset-level metadata
```

**Description:**
- `experiment/`  
  Raw sensor streams collected during the experiment (one CSV file per sensor).
- `accelerometer.csv`, `gyroscope.csv`, `location.csv`, etc.  
  Time-series sensor measurements with timestamps.
- `reference_journals.json`  
  Reference journals describing user behaviors and activity annotations.
- `metadata.csv`  
  Dataset-level metadata (e.g., session information, timestamps, and statistics).
