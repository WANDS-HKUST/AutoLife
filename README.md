<p align="center">
  <img src="img/autolife.jpg" alt="Project Logo" width="120" />
</p>

<h1 align="center">🚀 AutoLife Dataset: Automatic Life Journaling with Smartphones and LLMs</h1>

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
The widespread adoption of mobile devices, especially smartphones, has fundamentally transformed how people interact with the physical world and generate personal data. Modern phones continuously capture rich multimodal signals such as motion, location, and environmental context, enabling new opportunities to understand human behavior at scale.

**Life journaling** is an emerging application that aims to automatically generate semantic and factual descriptions of a person’s daily life from sensor data. Instead of relying on manual logging, life journaling systems can infer key activities, behaviors, transitions, and surrounding contexts, producing structured and natural summaries of daily experiences. Such capabilities enable a wide range of downstream applications, including personalized recommendations based on user behavior, automatic organization and annotation of personal photos and videos, analysis and optimization of daily routines for health and productivity, and long-term behavior understanding.

The **AutoLife Dataset** is designed to support research in automatic life journaling and mobile sensing. It contains multimodal smartphone sensor data aligned with **reference journals** describing user activities collected during a real-world campus user study. The dataset provides temporally synchronized sensor streams and human-readable annotations, enabling the development and evaluation of models for behavior recognition, temporal reasoning, multimodal fusion, and sensor-to-text generation.

This dataset serves as the official **benchmarking dataset** for our [IMWUT paper](https://dl.acm.org/doi/10.1145/3770683):  
👉 **“AutoLife: Automatic Life Journaling with Smartphone Sensors and Large Language Models”**  


---

## 📌 Dataset Overview

Each record contains:
- 📱 **Smartphone sensor data** collected during real-world usage
- 📝 **Reference journals** describing user behaviors and activities
- ⏱️ **Metadata** for setup

Example scenarios include campus mobility, indoor stays, short transitions, and daily routines.

### Basic Statistics

| Metric | Value |
|--------|-------|
| Total duration | 370.02 hours |
| Mean segment duration | 2.20 hours |
| Median segment duration | 1.78 hours |

---

## 📥 Download Dataset

The dataset is available at:

👉 [Download here](https://drive.google.com/file/d/16hXedIOmaIZJ82wbdIaJIiGSw6bEF_PU/view?usp=sharing)

After downloading, unzip the dataset:

```bash
unzip autolife_dataset.zip -d data/
```
Put the folder 'autolife_dataset' in the main directory of this repository.

## 📂 Dataset Structure
``` text
autolife_dataset/
├── experiment/                     // Raw sensor streams collected during the experiment
│   ├── time_tag_1/                 // Data collection session folder, named in 'HH_MM_SS' format
│   │   ├── accelerometer.csv       // Accelerometer measurements with timestamps
│   │   ├── gyroscope.csv           // Gyroscope measurements with timestamps
│   │   ├── location.csv            // Location samples with timestamps
│   │   ├── wifi.csv                // WiFi scan records with timestamps
│   │   ├── label.csv               // Experiment start/end time and segment labels
│   │   └── [other_sensor].csv      // Other available sensor modalities
│   ├── time_tag_2/
│   │   └── ...
reference_journals.json         // Reference journals describing user behaviors and activity annotations
metadata.csv                    // Dataset-level metadata and statistics
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

## ⚙️ Setup

We recommend Python 3.8+.

Install dependencies:
```bash
pip install -r requirements.txt
```
