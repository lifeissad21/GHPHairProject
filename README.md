
# 🧪 Shampoo pH vs. Hair Strength Analysis

This project investigates how shampoos of varying pH levels affect the tensile strength of keratin-based human hair samples. Using controlled solution exposure and precise data collection, we analyze structural changes in hair subjected to different pH environments.

[![Visit App](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit&logoColor=white)](https://ghphairproject.streamlit.app/)

## 📁 Project Structure
```
.
├── app.py                      # Main Streamlit app for interactive analysis
├── Combined\_Sample\_Data\_Sigfigs.csv  # Final combined dataset with 4 significant figures
├── CombinedSampleData/        # Aggregated CSV files by sample
├── Sample1\_TensileStrength/   # Raw CSV files for Sample 1 (S1)
├── Sample2\_TensileStrength/   # Raw CSV files for Sample 2 (S2)
├── Sample3\_TensileStrength/   # Raw CSV files for Sample 3 (S3)
├── Sample4\_TensileStrength/   # Raw CSV files for Sample 4 (S4)
├── SolutionsData/             # pH-specific solution data (acidic, neutral, basic)
├── pyproject.toml             # Python project dependencies and metadata
├── uv.lock                    # Dependency lock file (for `uv` or similar)
├── .python-version            # Python version control (for pyenv)
└── README.md                  # You're here!

```

## 🧬 Objective

To assess the **effect of shampoo pH** on **hair tensile strength**, simulating real-world hair care scenarios and quantifying how acidic or basic solutions alter the keratin fiber integrity.

## 🧫 Method Summary

- Human hair samples were divided into groups and submerged in shampoo solutions adjusted to specific pH values.
- pH groups include: **highly acidic**, **slightly acidic**, **neutral**, **slightly basic**, and **highly basic**.
- Exposure time: 24 hours.
- Post-treatment tensile strength was measured using a force sensor.
- Data was collected, cleaned, and combined for visualization and statistical analysis.

## 📊 Features

- Interactive dashboard built with **Streamlit**
- Auto-rounded data to **4 significant figures**
- Per-sample and per-treatment visualizations
- CSV + Excel input support
- Modular code for easy scaling and update

## 🚀 Getting Started

### Install Dependencies

```bash
# Option 1: Using uv
uv venv
uv pip install -r pyproject.toml

# Option 2: Using pip
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
````

### Run the App

```bash
streamlit run app.py
```

## 🧾 Data Overview

* `CombinedSampleData/`: Preprocessed per-sample datasets
* `SampleX_TensileStrength/`: Raw measurements for each hair sample and treatment stage
* `SolutionsData/`: pH levels and their measured effects

## 🧠 Analysis Goals

* Identify which pH levels result in significant tensile changes
* Visualize the degradation or strengthening patterns in hair fibers
* Provide evidence-based recommendations for optimal shampoo pH ranges

## 📌 Notes

* All data has been rounded to **four significant figures**
* Naming convention follows: `S[Sample#]T[Treatment#]_Data_[MMDDYYYY].csv`
* Charts and metrics generated dynamically through the dashboard

## 📃 License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

> For scientific posters or presentations, data from `Combined_Sample_Data_Sigfigs.csv` is recommended as the authoritative source.
