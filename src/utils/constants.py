"""
Project Constants
Multi-Touch Marketing Attribution & ROI Dashboard
"""

# Supported Marketing Channels
CHANNELS = [
    "Google Ads",
    "Facebook",
    "Instagram",
    "LinkedIn",
    "Email",
    "YouTube",
    "Twitter",
]

# KPI Names
KPIS = ["CTR", "CPC", "CPM", "ROI", "ROAS", "CAC", "Revenue", "Spend"]

# Attribution Models
ATTRIBUTION_MODELS = ["First Touch", "Last Touch", "Linear"]

# Report Names
REPORTS = {
    "EDA": "eda_report.csv",
    "FEATURED_DATASET": "featured_dataset.csv",
    "MASTER_DATASET": "master_dataset.csv",
    "ATTRIBUTION_RESULTS": "attribution_results.csv",
}

# Default Values
DEFAULT_ENCODING = "utf-8"
DEFAULT_DATE_FORMAT = "%Y-%m-%d"

# Dashboard Pages
DASHBOARD_PAGES = [
    "Executive Summary",
    "Campaign Analysis",
    "Channel Analysis",
    "Attribution Analysis",
    "Customer Journey Analysis",
]

# Logging Levels
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
