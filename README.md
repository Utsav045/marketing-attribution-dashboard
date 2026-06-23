# 📊 Marketing Attribution Dashboard

A Python-based project for multi-touch marketing attribution, customer journey construction, and ROI analytics. This repository includes data ingestion, preprocessing, attribution modeling, and test coverage for a robust analytics workflow.

---

## 🚀 Project Overview

This dashboard project is designed to:
- Ingest marketing raw datasets for ad spend, customer interactions, and conversions
- Clean and normalize data for analytics
- Build customer journey paths from interaction histories
- Calculate attribution using first-touch, last-touch, and linear attribution models
- Produce processed outputs for KPI and dashboard visualization

---

## 📁 Repository Structure

```text
.
├── data/
│   ├── raw/                        # Original source datasets
│   └── processed/                  # Cleaned and generated analytics outputs
├── docs/                          # Project documentation and progress logs
├── src/
│   ├── attribution/                # Attribution model implementations
│   ├── ingestion/                  # Data ingestion and load logic
│   ├── preprocessing/              # Data cleaning and transformation
│   ├── analytics/                  # KPI and analytics calculations
│   ├── database/                   # Postgres persistence and queries
│   └── visualization/              # Plotting and dashboard charts
├── tests/                         # Unit and regression tests
├── pyproject.toml                 # Python dependency and tooling config
└── README.md
```

---

## ✅ Key Features

- Data ingestion from raw CSV files
- Duplicate removal and missing-value handling
- Currency cleansing and date normalization
- Customer journey path generation
- First touch, last touch, and linear attribution
- Regression coverage for attribution logic
- Clean pytest discovery and execution

---

## 📌 Project Progress

### 11 June 2026
- Project onboarding and repository setup
- Team coordination and environment planning
- Defined initial workflow and task assignments

### 12 June 2026
- Dataset selection and evaluation
- Agreed to begin development with available data
- Established Git workflow and update cadence

### 13 June 2026
- Repository synchronization and structure updates
- Dependency installation and local setup guidance
- Confirmed team development process

### 16 June 2026
- Finalized project structure and module boundaries
- Started development work and assigned modules
- Reviewed documentation and development plan

### 20 June 2026
- Stabilized preprocessing modules and exports
- Fixed attribution revenue parsing for `$`-formatted values
- Locked pytest discovery to `tests/` only
- Added `tests/test_linear_attribution.py` regression coverage
- Confirmed end-to-end tests are passing

---

## 🧪 Test Instructions

Run the full test suite using the project virtual environment:

```bash
.\.venv\Scripts\python.exe -m pytest
```

If you are using pip, install dev tooling first:

```bash
pip install -r requirements.txt
pip install pytest
```

---

## ⚙️ Setup & Run

1. Activate your Python virtual environment.
2. Install project dependencies from `pyproject.toml` or `requirements.txt`.
3. Make sure the raw CSV files exist in `data/raw/`.
4. Run your preprocessing and attribution scripts as needed.

Example:

```bash
.\.venv\Scripts\python.exe src\preprocessing\data_cleaner.py
.\.venv\Scripts\python.exe src\preprocessing\transform_dates.py
.\.venv\Scripts\python.exe src\attribution\attribution_engine.py
.\.venv\Scripts\python.exe src\attribution\linear_attribution.py
```

---

## 📚 Documentation

Useful documentation files:
- `docs/Meeting_Notes.md` — team meeting summaries and decisions
- `docs/Project_Progress_Log.md` — consolidated daily progress log
- `docs/Python_Implementation.md` — implementation report and status
- `docs/Work_Distribution.md` — team roles and responsibilities

---

## 👥 Team

- **Utsav** — Team lead, architecture, integration, pipeline orchestration
- **Rajarshi** — Python development, data processing, analytics
- **Isaac** — SQL development, database design, query optimization
- **Palak** — Documentation, testing support, dataset research

---

## 🎯 Current Status

The repository is currently in a stable development state, with preprocessing and attribution logic fixed, tests passing, and the project ready to move into KPI engineering and dashboard preparation.
