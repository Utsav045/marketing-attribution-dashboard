# API Documentation

## Project

Multi Touch Marketing Attribution and ROI Analytics Dashboard

## Purpose of this Document

This document explains how the project modules, scripts and data flow work together. Although this project is not a live web API application, the term API documentation is used here to describe the internal application interfaces, module functions, script entry points and expected input and output files.

The project is designed as a Python based analytics workflow supported by SQL and dashboard reporting. The workflow moves from raw data ingestion to preprocessing, attribution modeling, KPI calculation, database storage and visualization output.

## Project Workflow Summary

The general workflow is:

Raw datasets are placed in the data folder.

The ingestion module loads the datasets.

The preprocessing module cleans and normalizes the datasets.

The attribution module builds attribution outputs.

The analytics module calculates marketing KPIs.

The database layer stores structured tables and reporting views.

The visualization layer prepares charts and dashboard outputs.

The testing layer validates the workflow.

## Main Data Inputs

The project expects three main input datasets.

## 1. Ad Spend Dataset

### Purpose

This dataset stores campaign level marketing cost and engagement data.

### Expected Fields

campaign_id
channel
spend
clicks
impressions
date

### Example Record

campaign_id: C001
channel: Google
spend: 1500
clicks: 300
impressions: 15000
date: 2026-06-01

## 2. Customer Journey Dataset

### Purpose

This dataset stores user interactions with marketing channels.

### Expected Fields

user_id
channel
interaction_time
campaign_id

### Example Record

user_id: U001
channel: Facebook
interaction_time: 2026-06-01 10:30:00
campaign_id: C002

## 3. Conversion Dataset

### Purpose

This dataset stores successful customer conversions and revenue values.

### Expected Fields

conversion_id
user_id
revenue
conversion_date

### Example Record

conversion_id: CV001
user_id: U001
revenue: 250
conversion_date: 2026-06-05 14:00:00

## Source Folder Structure

The main source code folders are:

src/ingestion
src/preprocessing
src/attribution
src/analytics
src/database
src/pipeline
src/visualization
src/utils

## Ingestion Module

### Folder

src/ingestion

### Purpose

The ingestion module is responsible for loading raw datasets into the project.

### Main Files

data_loader.py
load_csv.py
load_data.py
validate_schema.py

### Expected Functionality

Read CSV files.
Check whether files exist.
Load data into pandas DataFrames.
Validate that required columns are present.
Return loaded datasets for preprocessing.

### Expected Output

Cleanly loaded raw dataframes for:

Ad spend data
Customer journey data
Conversion data

## Preprocessing Module

### Folder

src/preprocessing

### Purpose

The preprocessing module cleans and transforms raw marketing datasets.

### Main Files

data_cleaner.py
feature_engineering.py
handle_missing.py
transform_dates.py

### Expected Functionality

Remove duplicate records.
Handle missing values.
Standardize channel names.
Clean currency formatted values.
Convert date fields into datetime format.
Create additional fields needed for analysis.

### Expected Output

Cleaned datasets ready for attribution and KPI analysis.

## Attribution Module

### Folder

src/attribution

### Purpose

The attribution module calculates how conversion credit should be shared across customer touchpoints.

### Main Files

attribution_engine.py
first_touch.py
last_touch.py
linear_attribution.py
position_based.py

### Attribution Models

First Touch Attribution
Last Touch Attribution
Linear Attribution
Time Decay Attribution
Position Based Attribution

## First Touch Attribution

### Description

First touch attribution assigns all conversion credit to the first customer interaction.

### Input

Customer journey data
Conversion data

### Output

Attribution table showing the first channel credited for each conversion.

## Last Touch Attribution

### Description

Last touch attribution assigns all conversion credit to the final customer interaction before conversion.

### Input

Customer journey data
Conversion data

### Output

Attribution table showing the final channel credited for each conversion.

## Linear Attribution

### Description

Linear attribution shares credit equally across all eligible touchpoints before conversion.

### Input

Customer journey data
Conversion data

### Output

Attribution table showing equal conversion credit distribution.

## Time Decay Attribution

### Description

Time decay attribution gives higher credit to touchpoints closer to conversion.

### Input

Customer journey data
Conversion data

### Output

Attribution table showing weighted credit based on time distance from conversion.

## Position Based Attribution

### Description

Position based attribution gives stronger credit to the first and last touchpoints, while the remaining credit is shared across middle touchpoints.

### Standard Logic

One touchpoint receives 100 percent credit.

Two touchpoints receive 50 percent each.

Three or more touchpoints use:

40 percent first touch
40 percent last touch
20 percent shared among middle touchpoints

## Analytics Module

### Folder

src/analytics

### Purpose

The analytics module calculates business KPIs and prepares outputs for dashboard reporting.

### Main Files

cac.py
conversation_date.py
eda.py
kpi_calculator.py
roas.py
roi.py

### KPIs Calculated

Total Spend
Total Revenue
Total Clicks
Total Impressions
CPC
CPM
CAC
Conversion Rate
ROAS
ROI
Revenue Per Customer
Attributed Revenue
Attribution Credit

## Database Module

### Folder

src/database and sql

### Purpose

The database layer stores staging tables, dimension tables, fact tables and reporting views.

### Main SQL Files

schema.sql
staging_tables.sql
attribution_queries.sql
kpi_queries.sql
dashboard_views.sql

### Database System

PostgreSQL

### Database Purpose

Store clean marketing data.
Sequence customer journeys.
Calculate attribution outputs.
Create dashboard reporting views.
Support monthly and weekly trend analysis.
Support advanced attribution models.

## Pipeline Module

### Folder

src/pipeline

### Purpose

The pipeline module coordinates the full execution workflow.

### Main Files

orchestrator.py
run_pipeline.py

### Expected Workflow

Load raw data.
Validate schema.
Clean and transform data.
Build customer journeys.
Run attribution models.
Calculate KPIs.
Generate outputs.
Prepare results for visualization.

## Visualization Module

### Folder

src/visualization

### Purpose

The visualization module creates plots and chart outputs from processed analytics data.

### Main Files

charts.py
plot_campaigns.py
plot_channels.py
plot_roi.py

### Expected Visual Outputs

Channel performance chart
Campaign performance chart
ROI chart
ROAS chart
Attribution model comparison chart
Monthly trend chart
Weekly trend chart

## Testing Endpoints and Commands

This project uses local test commands instead of HTTP API endpoints.

## Run Full Test Suite

```bash
python -m pytest
```

## Run With Windows Virtual Environment

```bash
.\.venv\Scripts\python.exe -m pytest
```

## Run Preprocessing Script

```bash
.\.venv\Scripts\python.exe src\preprocessing\data_cleaner.py
```

## Run Date Transformation Script

```bash
.\.venv\Scripts\python.exe src\preprocessing\transform_dates.py
```

## Run Attribution Engine

```bash
.\.venv\Scripts\python.exe src\attribution\attribution_engine.py
```

## Run Linear Attribution

```bash
.\.venv\Scripts\python.exe src\attribution\linear_attribution.py
```

## Run Pipeline

```bash
.\.venv\Scripts\python.exe src\pipeline\run_pipeline.py
```

## Expected Processed Outputs

The project can generate processed files for:

Cleaned ad spend data
Cleaned customer journey data
Cleaned conversion data
Customer journey paths
Attribution output
KPI output
Dashboard ready summary tables

## SQL Reporting Views

The database layer provides views for dashboard consumption.

Important views include:

vw_monthly_marketing_trends
vw_weekly_marketing_trends
vw_attribution_model_comparison
vw_channel_roi_by_model
vw_executive_sql_summary

## Error Handling Expectations

The project should handle:

Missing files
Missing required columns
Invalid date formats
Duplicate records
Missing user IDs
Missing campaign IDs
Invalid spend values
Invalid revenue values
Empty datasets
Unsupported attribution model names

## Security and Data Privacy

Raw data files should not be pushed directly to GitHub. Sensitive files, large datasets, environment variables and database credentials should remain excluded through .gitignore.

## Documentation Summary

This documentation explains how the project modules interact. The project does not depend on a live HTTP API at this stage, but its internal scripts and modules serve as the application interface for data ingestion, transformation, attribution modeling, KPI calculation and dashboard reporting.

## Conclusion

The project API structure supports a complete analytics workflow from raw marketing data to actionable dashboard insights. It provides reusable modules for ingestion, preprocessing, attribution, analytics, database reporting, testing and visualization.
