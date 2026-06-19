# Architecture

## Project Flow

1. Raw Datasets
2. Data Loading (`data_loader.py`)
3. Data Preprocessing
   - `data_cleaner.py`
   - `handle_missing.py`
   - `transform_dates.py`
4. Feature Engineering
5. Attribution Models
   - First Touch
   - Last Touch
   - Linear Attribution
6. KPI Calculation
   - ROI
   - ROAS
   - CTR
   - CPC
   - CPA
7. Dashboard Dataset Generation
8. Power BI Dashboard
9. Final Reports