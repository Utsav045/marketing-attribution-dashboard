# Testing Reports

## Project: Marketing Attribution Dashboard 

### **Date:** 8 July 2026

---
# 1. Testing Overview

The project testing was conducted to verify the functionality, accuracy, and integration of all major project components, including SQL database operations, Python analytics modules, and the Power BI dashboard. The objective was to ensure that all implemented features operate correctly and produce accurate analytical results.

---

# 2. SQL Testing

## Testing Period

**26 June 2026 – 8 July 2026**

## Objective

To verify the correctness of the database schema, SQL scripts, attribution models, KPI calculations, and dashboard views throughout the implementation phase.

### SQL Testing Timeline

#### 26 June 2026
- Verified database schema creation.
- Tested table creation, primary keys, foreign keys, and relationships.
- Validated successful import of campaign, customer journey, spend, and revenue datasets.

#### 27 June 2026
- Tested attribution query implementation.
- Verified customer journey processing.
- Checked campaign mapping and revenue consistency.

#### 28 June 2026
- Validated KPI query calculations.
- Tested marketing spend analysis.
- Verified revenue aggregation queries.

#### 29 June 2026
- Tested SQL dashboard views.
- Validated JOIN operations between all project tables.
- Checked SQL query execution performance.

#### 30 June – 5 July 2026
- Performed continuous SQL validation.
- Fixed minor query issues.
- Optimized SQL scripts for dashboard integration.
- Revalidated generated outputs.

#### 6 July 2026
- Reviewed SQL implementation before final integration.
- Verified database schema, attribution queries, KPI queries, and dashboard views.

#### 7 July 2026
- Revalidated SQL scripts after repository synchronization.
- Confirmed compatibility with Python analytics modules.

#### 8 July 2026
- Performed final SQL validation.
- Verified dashboard data consistency.
- Confirmed successful SQL integration with the Power BI dashboard.

### SQL Components Tested

- schema.sql
- attribution_queries.sql
- kpi_queries.sql
- dashboard_views.sql

### Test Results

| Test Case | Status |
|-----------|--------|
| Database Schema | ✅ Passed |
| Dataset Import | ✅ Passed |
| Table Relationships | ✅ Passed |
| Attribution Queries | ✅ Passed |
| KPI Queries | ✅ Passed |
| Dashboard Views | ✅ Passed |
| SQL Joins | ✅ Passed |
| Data Validation | ✅ Passed |

### Result

All SQL components executed successfully and produced accurate analytical results throughout the development period.

---

# 3. Python Module Testing

## Testing Period

**26 June 2026 – 8 July 2026**

## Objective

To validate Python analytics modules, visualization scripts, ROI calculations, and integration with SQL data.

### Python Testing Timeline

#### 26 June 2026
- Configured Python analytics environment.
- Verified dataset loading.
- Tested initial analytics scripts.

#### 27 June 2026
- Validated channel analytics implementation.
- Tested data preprocessing.
- Verified processed outputs.

#### 28 June 2026
- Tested campaign visualization module.
- Verified campaign charts.

#### 29 June 2026
- Tested channel visualization module.
- Verified generated charts and analytics.

#### 30 June – 5 July 2026
- Performed continuous module testing.
- Improved visualization outputs.
- Fixed minor implementation issues.
- Revalidated analytics results.

#### 6 July 2026
- Completed testing of channel.py.
- Verified integration with SQL analytics.

#### 7 July 2026
- Completed ROI visualization (plot_roi.py).
- Tested ROI calculations.
- Verified generated ROI charts.

#### 8 July 2026
- Performed final validation of all Python modules.
- Verified SQL integration.
- Confirmed compatibility with the Power BI dashboard.

### Python Modules Tested

| Module | Description | Status |
|---------|-------------|--------|
| channel.py | Channel Performance Analytics | ✅ Passed |
| plot_channel.py | Channel Visualization | ✅ Passed |
| plot_campaign.py | Campaign Performance Visualization | ✅ Passed |
| plot_roi.py | ROI Visualization | ✅ Passed |

### Functional Testing

- Dataset loading validated.
- Analytics executed successfully.
- Charts generated correctly.
- ROI calculations verified.
- Campaign analytics validated.
- Channel performance analysis verified.

### Integration Testing

- SQL data imported successfully into Python.
- Analytics calculations executed correctly.
- Visualization modules displayed expected outputs.
- Generated charts matched SQL query results.
- Python analytics integrated successfully with the Power BI dashboard.

### Result

All Python analytics modules executed successfully without runtime errors and produced accurate analytical outputs throughout the implementation period.