# Isaac SQL Implementation Report

## Project Area

Multi Touch Marketing Attribution and ROI Analytics Dashboard

## Developer

Isaac

## Assigned Role

Isaac handled database design, SQL development, attribution logic, advanced attribution models, trend analysis, stored procedures and SQL validation.

## Database Design

The database was designed using a star schema. The staging tables hold raw marketing data, while dimension and fact tables support business intelligence reporting.

## Main Tables

### Staging Tables

stg_ad_spend  
stg_customer_journey  
stg_conversions  

### Dimension Tables

dim_channel  
dim_campaign  
dim_customer  
dim_date  

### Fact Tables

fact_ad_spend  
fact_touchpoints  
fact_conversions  
fact_attribution  

## Advanced SQL Tasks Completed

### Monthly and Weekly Trend Analysis

Monthly and weekly trend views were created to help the team explain revenue, spend, ROAS, ROI, CPC and CPM over time.

Views created:

vw_monthly_marketing_trends  
vw_weekly_marketing_trends  

### Time Decay Attribution

Time decay attribution gives more credit to marketing touchpoints closer to the conversion date. This helps the business understand which recent interactions influenced customer purchase decisions.

### Position Based Attribution

Position based attribution gives 40 percent credit to the first touchpoint, 40 percent credit to the last touchpoint and 20 percent credit to middle touchpoints. This shows both awareness and closing influence.

### Stored Procedures

Stored procedures were created to refresh advanced attribution results automatically.

Procedures created:

sp_refresh_time_decay_attribution  
sp_refresh_position_based_attribution  
sp_refresh_all_advanced_attribution  

### Advanced Reporting Views

The reporting views were created for Power BI and dashboard integration.

Views created:

vw_attribution_model_comparison  
vw_channel_roi_by_model  
vw_executive_sql_summary  

## How This Supports Visualization

The dashboard can connect directly to the SQL views. These views provide clean results for model comparison, channel ROI, monthly trends and weekly trends.

## Explanation During Presentation

This SQL work proves that the project goes beyond basic Python processing. It adds database modeling, business intelligence preparation, attribution logic and automated refresh procedures.

The advanced SQL layer allows the dashboard to answer business questions such as:

Which channel performs best under each attribution model?  
Which channel has the highest ROAS?  
Which channel has the lowest CAC?  
How does performance change weekly or monthly?  
How does time decay attribution differ from first touch and last touch attribution?  