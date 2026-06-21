from pathlib import Path

# Project Root Directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Data Directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Reports Directory
REPORTS_DIR = PROJECT_ROOT / "reports"

# Dashboard Directory
DASHBOARD_DIR = PROJECT_ROOT / "dashboards"

# Dataset Files
AD_SPEND_FILE = RAW_DATA_DIR / "Add_Spend_Dataset.csv"
INTERACTION_FILE = RAW_DATA_DIR / "Customer_Interaction_Dataset.csv"
REVENUE_FILE = RAW_DATA_DIR / "Revenue_dataset.csv"

# Processed Files
FEATURED_DATASET = PROCESSED_DATA_DIR / "featured_dataset.csv"
MASTER_DATASET = PROCESSED_DATA_DIR / "master_dataset.csv"

# Logging
LOG_FILE = PROJECT_ROOT / "project.log"