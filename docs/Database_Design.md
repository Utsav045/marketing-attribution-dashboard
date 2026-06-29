# Database Design Documentation

## Project

Multi Touch Marketing Attribution and ROI Analytics Dashboard

## Developer

Isaac

## Purpose of the Database Design

The database layer was designed to support clean storage, transformation and reporting of marketing attribution data. The project works with three major data sources: ad spend data, customer journey data and conversion data. These datasets need to be organized in a way that makes attribution modeling, KPI calculation and dashboard visualization accurate and easy to maintain.

The database design follows an analytical structure. Raw data is first loaded into staging tables. After cleaning and validation, the data is transformed into dimension and fact tables. This structure supports fast reporting in Power BI and makes it easier to calculate marketing metrics such as CAC, ROAS, ROI, CPC and conversion credit.

## Database Technology

PostgreSQL is used as the main relational database system for this project. PostgreSQL was selected because it supports structured data storage, SQL joins, window functions, views, stored procedures, indexing and analytical queries.

## Database Schema

The database uses a schema named:

```sql
marketing
```

This schema contains staging tables, dimension tables, fact tables and reporting views.

## Data Sources

The database is designed around three main datasets.

### Ad Spend Dataset

This dataset contains campaign cost and performance data.

Expected fields:

```text
campaign_id
channel
spend
clicks
impressions
date
```

### Customer Journey Dataset

This dataset contains customer interactions across marketing channels.

Expected fields:

```text
user_id
channel
interaction_time
campaign_id
```

### Conversion Dataset

This dataset contains successful conversion records and revenue values.

Expected fields:

```text
conversion_id
user_id
revenue
conversion_date
```

## Staging Layer

The staging layer stores raw or lightly cleaned data before transformation into the analytical model.

### stg_ad_spend

This table stores raw campaign spend records.

Important columns:

```text
campaign_id
channel
spend
clicks
impressions
spend_date
```

### stg_customer_journey

This table stores all user marketing interactions before conversion.

Important columns:

```text
journey_id
user_id
channel
interaction_time
campaign_id
```

### stg_conversions

This table stores customer conversion and revenue records.

Important columns:

```text
conversion_id
user_id
revenue
conversion_date
```

## Dimensional Model

The analytical database uses a star schema design. The star schema separates descriptive information into dimension tables and measurable business events into fact tables.

This design improves reporting performance and makes the dashboard easier to connect to.

## Dimension Tables

### dim_channel

This table stores unique marketing channels such as Google, Facebook, Email, LinkedIn, Instagram and YouTube.

Main columns:

```text
channel_key
channel_name
```

### dim_campaign

This table stores campaign level information.

Main columns:

```text
campaign_key
campaign_id
campaign_name
channel_key
```

### dim_customer

This table stores unique customers or users.

Main columns:

```text
customer_key
user_id
```

### dim_date

This table supports time based reporting.

Main columns:

```text
date_key
full_date
day_number
week_number
month_number
month_name
quarter_number
year_number
```

## Fact Tables

### fact_ad_spend

This table stores campaign spend, clicks and impressions.

Main columns:

```text
ad_spend_key
campaign_key
channel_key
date_key
spend
clicks
impressions
```

### fact_touchpoints

This table stores ordered customer interactions.

Main columns:

```text
touchpoint_key
customer_key
campaign_key
channel_key
interaction_time
touchpoint_order
```

The touchpoint_order column is important because it helps determine first touch, middle touch and last touch positions in the customer journey.

### fact_conversions

This table stores successful customer conversions.

Main columns:

```text
conversion_key
conversion_id
customer_key
conversion_date
revenue
```

### fact_attribution

This table stores the output of attribution models.

Main columns:

```text
attribution_key
conversion_key
touchpoint_key
customer_key
campaign_key
channel_key
attribution_model
attribution_weight
attributed_revenue
```

This table allows the project to compare first touch, last touch, linear, time decay and position based attribution models.

## Star Schema Relationship

The relationship design is:

```text
dim_channel      → fact_ad_spend
dim_channel      → fact_touchpoints
dim_channel      → fact_attribution

dim_campaign     → fact_ad_spend
dim_campaign     → fact_touchpoints
dim_campaign     → fact_attribution

dim_customer     → fact_touchpoints
dim_customer     → fact_conversions
dim_customer     → fact_attribution

dim_date         → fact_ad_spend
```

## Customer Journey Sequencing

Customer journey sequencing is performed using SQL window functions. The system orders each user interaction by interaction_time.

Example logic:

```sql
ROW_NUMBER() OVER (
    PARTITION BY user_id
    ORDER BY interaction_time
) AS touchpoint_order
```

This allows the project to identify the first marketing interaction, the last marketing interaction and all middle interactions before conversion.

## Attribution Logic Supported by the Database

The database supports the following attribution models:

### First Touch Attribution

The first customer interaction receives 100 percent of the conversion credit.

### Last Touch Attribution

The final customer interaction before conversion receives 100 percent of the conversion credit.

### Linear Attribution

All customer touchpoints before conversion share the conversion credit equally.

### Time Decay Attribution

Touchpoints closer to the conversion date receive more credit than older touchpoints.

### Position Based Attribution

The first and last touchpoints receive the highest credit, while middle touchpoints share the remaining credit.

## Reporting Views

The database includes reporting views for dashboard use.

Important views include:

```text
vw_monthly_marketing_trends
vw_weekly_marketing_trends
vw_attribution_model_comparison
vw_channel_roi_by_model
vw_executive_sql_summary
```

These views help Power BI display trend analysis, channel performance, attribution comparison and executive level summaries.

## Indexing Strategy

Indexes are used to improve query performance on frequently joined and filtered columns.

Important indexes include:

```text
customer_key index on fact_touchpoints
interaction_time index on fact_touchpoints
customer_key index on fact_conversions
attribution_model index on fact_attribution
channel_key index on fact_attribution
```

## Data Quality Controls

The database design includes checks for:

Missing campaign IDs
Missing user IDs
Missing revenue values
Duplicate conversions
Unstandardized channel names
Touchpoints without channels
Conversions without attribution
Attribution weights that do not add up to 1.0
Attributed revenue that does not match original conversion revenue

## Business Value of the Database Design

The database design helps the project move from raw marketing data to reliable business intelligence. It supports accurate attribution modeling, KPI calculation, dashboard reporting and marketing decision making.

With this database layer, the project can answer questions such as:

Which channel creates the highest revenue?
Which channel has the best ROAS?
Which channel has the lowest CAC?
How does revenue change monthly or weekly?
How does attribution change under different models?
Which campaign should receive more or less budget?

## Conclusion

The database design provides a structured foundation for the marketing attribution dashboard. It organizes raw data into an analytical model that supports SQL attribution logic, KPI calculation, reporting views and executive dashboard visualization.
