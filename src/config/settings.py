"""
Application Settings
Multi-Touch Marketing Attribution & ROI Dashboard

Centralizes all configurable parameters — loaded from environment variables
with sensible defaults so the project works out-of-the-box.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

# ---------------------------------------------------------------------------
# Project Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
DASHBOARDS_DIR = PROJECT_ROOT / "dashboards"
SQL_DIR = PROJECT_ROOT / "sql"
LOG_FILE = PROJECT_ROOT / "project.log"

# ---------------------------------------------------------------------------
# Database Settings  (from .env)
# ---------------------------------------------------------------------------
DB_HOST: str = os.getenv("DB_HOST", "localhost")
DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
DB_NAME: str = os.getenv("DB_NAME", "marketing_attribution")
DB_USER: str = os.getenv("DB_USER", "postgres")
DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")

# ---------------------------------------------------------------------------
# Dataset Filenames
# ---------------------------------------------------------------------------
AD_SPEND_FILE: str = "add_spend_dataset.csv"
INTERACTION_FILE: str = "customer_interaction_dataset.csv"
REVENUE_FILE: str = "revenue_dataset.csv"

# Processed output filenames
CLEANED_AD_SPEND: str = "cleaned_add_spend_dataset.csv"
CLEANED_INTERACTION: str = "cleaned_customer_interaction_dataset.csv"
CLEANED_REVENUE: str = "cleaned_revenue_dataset.csv"

FEATURED_AD_SPEND: str = "adspend_featured.csv"
FEATURED_INTERACTION: str = "interaction_featured.csv"
FEATURED_REVENUE: str = "revenue_featured.csv"

ROI_RESULTS: str = "roi_results.csv"
ROAS_RESULTS: str = "roas_results.csv"
ATTRIBUTION_RESULTS: str = "attribution_results.csv"

# ---------------------------------------------------------------------------
# Pipeline Settings
# ---------------------------------------------------------------------------
MISSING_VALUE_STRATEGY: str = "fill_zero"   # Options: 'fill_zero', 'drop', 'fill_mean'
DATE_FORMAT: str = "%Y-%m-%d"
DEFAULT_ENCODING: str = "utf-8"

# ---------------------------------------------------------------------------
# Visualization Settings
# ---------------------------------------------------------------------------
FIGURE_DPI: int = 150
FIGURE_SIZE_DEFAULT: tuple[int, int] = (10, 6)
CHART_STYLE: str = "seaborn-v0_8-whitegrid"

# ---------------------------------------------------------------------------
# Attribution Model Settings
# ---------------------------------------------------------------------------
SUPPORTED_ATTRIBUTION_MODELS: list[str] = [
    "first_touch",
    "last_touch",
    "linear",
    "time_decay",
    "position_based",
]
TIME_DECAY_HALF_LIFE_DAYS: int = 7

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
