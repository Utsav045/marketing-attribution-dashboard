# Testing Report

## Project

Multi Touch Marketing Attribution and ROI Analytics Dashboard

## Purpose of Testing

Testing is carried out to confirm that the marketing attribution dashboard works correctly from data ingestion to final KPI reporting. The goal of testing is to ensure that the data is clean, attribution calculations are accurate, KPIs are correct and dashboard views produce reliable results.

Testing also helps confirm that Python scripts, SQL queries and reporting outputs are consistent with the business objectives of the project.

## Testing Scope

The testing scope covers:

Data ingestion testing
Data cleaning testing
Date transformation testing
Missing value handling
Customer journey construction testing
Attribution model testing
KPI calculation testing
SQL validation testing
Pipeline execution testing
Dashboard data validation

## Testing Tools

The project uses the following testing tools:

Python
Pytest
PostgreSQL
SQL validation queries
VS Code terminal
GitHub Actions
Power BI validation checks

## Test Environment

The project is tested locally using:

VS Code
Python virtual environment
PostgreSQL database
Project test folder
Pytest command line execution

Main test command:

```bash
python -m pytest
```

For Windows virtual environment:

```bash
.\.venv\Scripts\python.exe -m pytest
```

## Test Areas

## 1. Data Ingestion Testing

### Objective

To confirm that raw marketing datasets can be loaded successfully into the project.

### Expected Result

The system should load ad spend, customer journey and conversion datasets without breaking.

### Test Checks

CSV files are readable.
Required columns are present.
Empty files are rejected.
Incorrect file paths are handled properly.
Loaded data returns a valid dataframe.

## 2. Schema Validation Testing

### Objective

To confirm that input datasets contain the expected columns.

### Expected Columns

### Ad Spend Dataset

```text
campaign_id
channel
spend
clicks
impressions
date
```

### Customer Journey Dataset

```text
user_id
channel
interaction_time
campaign_id
```

### Conversion Dataset

```text
conversion_id
user_id
revenue
conversion_date
```

### Expected Result

The validation script should identify missing or wrongly named columns before analysis begins.

## 3. Data Cleaning Testing

### Objective

To confirm that the cleaning process handles duplicates, missing values and inconsistent formats.

### Test Checks

Duplicate records are removed.
Missing user IDs are handled.
Missing campaign IDs are detected.
Currency symbols are removed from revenue and spend fields.
Channel names are standardized.
Text fields are trimmed.
Numeric columns are converted correctly.

### Expected Result

The cleaned dataset should be suitable for attribution modeling and KPI calculation.

## 4. Date Transformation Testing

### Objective

To confirm that all date fields are converted into the correct datetime format.

### Fields Tested

```text
date
interaction_time
conversion_date
```

### Expected Result

Date fields should be converted successfully and should support monthly and weekly trend analysis.

## 5. Customer Journey Testing

### Objective

To confirm that the customer journey is built in the correct order.

### Test Logic

Each customer interaction should be sorted by interaction time.

### Expected Result

The first interaction should appear before middle interactions and the final interaction should appear before or on the conversion date.

### SQL Validation Example

```sql
SELECT
    customer_key,
    touchpoint_key,
    interaction_time,
    touchpoint_order
FROM fact_touchpoints
ORDER BY customer_key, touchpoint_order;
```

## 6. First Touch Attribution Testing

### Objective

To confirm that first touch attribution assigns 100 percent credit to the first touchpoint.

### Expected Result

For each conversion, only the first eligible touchpoint should receive full attribution credit.

### Validation Rule

```text
Total attribution weight per conversion = 1.0
```

## 7. Last Touch Attribution Testing

### Objective

To confirm that last touch attribution assigns 100 percent credit to the final touchpoint before conversion.

### Expected Result

For each conversion, only the last eligible touchpoint should receive full attribution credit.

## 8. Linear Attribution Testing

### Objective

To confirm that linear attribution distributes credit equally across all eligible touchpoints.

### Example

If a conversion has four touchpoints, each touchpoint should receive:

```text
1 / 4 = 0.25
```

### Expected Result

The sum of all linear attribution weights for each conversion should equal 1.0.

## 9. Time Decay Attribution Testing

### Objective

To confirm that time decay attribution gives more weight to touchpoints closer to conversion.

### Expected Result

Recent touchpoints should receive higher attribution weights than older touchpoints.

### Validation Rule

```text
Total attribution weight per conversion = 1.0
```

## 10. Position Based Attribution Testing

### Objective

To confirm that position based attribution gives higher credit to the first and last touchpoints.

### Expected Weighting Logic

One touchpoint:

```text
100 percent credit
```

Two touchpoints:

```text
50 percent first touch
50 percent last touch
```

Three or more touchpoints:

```text
40 percent first touch
40 percent last touch
20 percent shared by middle touchpoints
```

### Expected Result

The total attribution weight per conversion should equal 1.0.

## 11. KPI Testing

### Objective

To confirm that business metrics are calculated correctly.

### KPIs Tested

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

### Expected Result

The KPI outputs should match the formulas defined in the KPI documentation.

## 12. SQL Validation Testing

### Objective

To confirm that SQL outputs are accurate and consistent.

### Attribution Weight Test

```sql
SELECT
    conversion_key,
    attribution_model,
    ROUND(SUM(attribution_weight), 4) AS total_weight
FROM fact_attribution
GROUP BY conversion_key, attribution_model
HAVING ROUND(SUM(attribution_weight), 4) <> 1.0000;
```

Expected result:

```text
No rows returned
```

### Revenue Allocation Test

```sql
SELECT
    fa.conversion_key,
    fa.attribution_model,
    ROUND(fc.revenue, 2) AS original_revenue,
    ROUND(SUM(fa.attributed_revenue), 2) AS allocated_revenue
FROM fact_attribution fa
JOIN fact_conversions fc
    ON fc.conversion_key = fa.conversion_key
GROUP BY
    fa.conversion_key,
    fa.attribution_model,
    fc.revenue;
```

Expected result:

```text
Allocated revenue should match original conversion revenue for each attribution model.
```

### Duplicate Attribution Test

```sql
SELECT
    conversion_key,
    touchpoint_key,
    attribution_model,
    COUNT(*) AS duplicate_count
FROM fact_attribution
GROUP BY
    conversion_key,
    touchpoint_key,
    attribution_model
HAVING COUNT(*) > 1;
```

Expected result:

```text
No duplicate rows should be returned.
```

## 13. Dashboard Validation

### Objective

To confirm that Power BI visuals match SQL output.

### Test Checks

Dashboard total revenue matches SQL total revenue.
Dashboard total spend matches SQL total spend.
ROAS in Power BI matches SQL ROAS.
ROI in Power BI matches SQL ROI.
Channel ranking is consistent with SQL output.
Monthly trend chart matches SQL monthly view.
Weekly trend chart matches SQL weekly view.

## Test Result Summary

| Test Area                   | Expected Status                                        |
| --------------------------- | ------------------------------------------------------ |
| Data ingestion              | Passed after valid datasets are loaded                 |
| Schema validation           | Passed if all required fields exist                    |
| Data cleaning               | Passed if duplicates and invalid values are handled    |
| Date transformation         | Passed if date fields are valid                        |
| Customer journey sequencing | Passed if touchpoints are ordered correctly            |
| First touch attribution     | Passed if first touch receives full credit             |
| Last touch attribution      | Passed if last touch receives full credit              |
| Linear attribution          | Passed if credit is equally shared                     |
| Time decay attribution      | Passed if recent touches receive higher credit         |
| Position based attribution  | Passed if first and last touches receive higher credit |
| KPI calculations            | Passed if formulas match documentation                 |
| SQL validation              | Passed if no weight or revenue errors are returned     |
| Dashboard validation        | Passed if Power BI values match SQL views              |

## Known Testing Notes

The project should not upload raw datasets directly into GitHub. Data files should remain excluded where required. Testing should focus on code, SQL logic, documentation and reproducible execution.

## Conclusion

Testing confirms that the marketing attribution dashboard is reliable, reproducible and suitable for business reporting. The testing process checks the accuracy of data cleaning, attribution modeling, KPI calculation and dashboard outputs.
