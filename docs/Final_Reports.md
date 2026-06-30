# Final Project Report

## Project Title

Multi Touch Marketing Attribution and ROI Analytics Dashboard

## Project Type

Data Analytics and Business Intelligence Project

## Project Duration

4 Weeks

## Executive Summary

The Multi Touch Marketing Attribution and ROI Analytics Dashboard was developed to solve a common marketing analytics problem. Businesses often spend money across several advertising channels, but they do not always know which channels truly contribute to revenue. Traditional last click attribution gives all conversion credit to the final customer interaction. This can mislead marketing teams and cause poor budget allocation.

This project provides a more complete solution by combining data ingestion, preprocessing, customer journey construction, attribution modeling, KPI calculation, SQL database design and dashboard reporting. The system supports multiple attribution models, including first touch, last touch, linear, time decay and position based attribution.

The final dashboard is designed to help marketing managers compare channels, measure return on ad spend, identify wasteful campaigns and make better budget decisions.

## Business Problem

Marketing teams need accurate insight into how channels contribute to conversions. A customer may first see a Facebook ad, later click a Google ad, then receive an email before finally purchasing. If the business uses only last click attribution, all the revenue may be credited to the email campaign while Facebook and Google receive no credit.

This creates several problems:

Incorrect ROI calculation
Poor campaign optimization
Wrong channel ranking
Budget misallocation
Inaccurate customer acquisition cost
Weak understanding of the customer journey

The project addresses these issues by distributing conversion credit across customer touchpoints using multiple attribution models.

## Project Aim

The aim of this project is to build a marketing attribution analytics dashboard that can process marketing data, construct customer journeys, apply attribution models, calculate KPIs and present actionable insights for business decision making.

## Project Objectives

The objectives are to:

Ingest marketing datasets from raw files.
Clean and normalize marketing data.
Validate dataset structure and required columns.
Build ordered customer journey paths.
Apply first touch, last touch and linear attribution models.
Extend the project with time decay and position based attribution.
Calculate marketing KPIs including CPC, CPM, CAC, ROAS and ROI.
Design PostgreSQL tables and SQL reporting views.
Prepare dashboard ready outputs for visualization.
Provide testing and documentation for reproducibility.

## Project Architecture

The project follows a modular analytics architecture.

Raw data is stored in the data folder.
The ingestion module loads the datasets.
The preprocessing module cleans and transforms the data.
The attribution module calculates conversion credit.
The analytics module calculates KPIs.
The database layer stores structured data and reporting views.
The visualization layer creates charts and dashboard outputs.
The testing layer confirms accuracy.

## Data Sources

The project uses three main datasets.

## Ad Spend Data

This contains campaign costs, clicks and impressions.

Fields include:

campaign_id
channel
spend
clicks
impressions
date

## Customer Journey Data

This contains user level marketing interactions.

Fields include:

user_id
channel
interaction_time
campaign_id

## Conversion Data

This contains revenue and conversion information.

Fields include:

conversion_id
user_id
revenue
conversion_date

## Data Cleaning and Preprocessing

The preprocessing stage prepares the raw data for analysis. The cleaning tasks include:

Removing duplicate records
Handling missing values
Standardizing channel names
Cleaning currency formatted values
Converting date fields to datetime format
Validating required columns
Preparing datasets for attribution modeling

This stage is important because poor data quality can lead to incorrect attribution results and unreliable dashboard outputs.

## Customer Journey Construction

Customer journey construction arranges each customer's interactions in time order. This makes it possible to identify the first touchpoint, last touchpoint and middle touchpoints.

The journey logic supports the attribution engine by showing how each user moved through different channels before converting.

## Attribution Models Implemented

## First Touch Attribution

First touch attribution assigns all conversion credit to the first marketing channel that interacted with the customer. This model is useful for identifying channels that create awareness.

## Last Touch Attribution

Last touch attribution assigns all conversion credit to the last channel before conversion. This model is useful for identifying channels that close sales.

## Linear Attribution

Linear attribution distributes conversion credit equally across all customer touchpoints. This model is useful when all touchpoints are considered equally important.

## Time Decay Attribution

Time decay attribution gives more credit to touchpoints closer to conversion. This model is useful when recent interactions are believed to have stronger influence on purchase decisions.

## Position Based Attribution

Position based attribution gives higher credit to the first and last touchpoints. In this project, the standard logic is 40 percent for the first touchpoint, 40 percent for the last touchpoint and 20 percent shared across middle touchpoints.

## SQL and Database Development

The database layer was developed to support structured analytics and dashboard reporting. The database uses staging tables, dimension tables and fact tables.

Staging tables hold raw imported data.

Dimension tables store channels, campaigns, customers and dates.

Fact tables store ad spend, touchpoints, conversions and attribution outputs.

Reporting views prepare clean results for dashboard visualization.

## Key SQL Work Completed

Database schema design
Staging table creation
Star schema design
Customer journey sequencing
Attribution model queries
Monthly trend analysis
Weekly trend analysis
KPI calculation queries
Time decay attribution SQL
Position based attribution SQL
Stored procedures
Dashboard reporting views
SQL validation tests

## KPI Calculations

The dashboard calculates the following KPIs:

Total Spend
Total Revenue
Total Clicks
Total Impressions
Cost Per Click
Cost Per Thousand Impressions
Customer Acquisition Cost
Conversion Rate
Return on Ad Spend
Return on Investment
Revenue Per Customer
Attributed Revenue
Attribution Credit

## Dashboard Pages

## Executive Overview

This page summarizes total revenue, total spend, conversions, ROAS, ROI and CAC.

## Attribution Analysis

This page compares revenue allocation across different attribution models.

## Channel Performance

This page ranks channels based on spend, revenue, CAC, ROAS and ROI.

## Trend Analysis

This page shows weekly and monthly performance trends.

## Campaign Performance

This page identifies strong and weak campaigns for budget decision making.

## Testing and Validation

The project includes testing for:

Data loading
Schema validation
Data cleaning
Date transformation
Customer journey construction
Attribution model accuracy
KPI calculations
SQL validation
Dashboard result consistency

Attribution validation checks whether each conversion has a total attribution weight of 1.0 under each model. Revenue validation checks whether allocated revenue matches the original conversion revenue.

## Project Outcomes

At the end of the project, the system is expected to deliver:

Clean marketing datasets
Customer journey paths
Attribution outputs
KPI tables
SQL reporting views
Dashboard visuals
Testing reports
Project documentation
Business recommendations

## Business Insights Expected

The dashboard is expected to help answer questions such as:

Which marketing channel produces the highest attributed revenue?
Which channel has the best ROAS?
Which channel has the lowest CAC?
Which campaigns should receive more budget?
Which campaigns should be reduced or paused?
How does channel performance change monthly or weekly?
How do different attribution models change the understanding of channel value?

## Recommendations

Marketing teams should not rely only on last click attribution because it can hide the contribution of earlier touchpoints. The project should compare multiple attribution models before making budget decisions.

Channels with high ROAS and low CAC should be considered for budget increase.

Channels with high spend and low attributed revenue should be reviewed or optimized.

Time based trends should be monitored regularly to identify performance changes.

Attribution outputs should be validated before being used for executive reporting.

## Limitations

The project uses available marketing datasets rather than live advertising API data.

The dashboard depends on the quality and completeness of the input datasets.

Attribution models provide analytical estimates and should be interpreted with business context.

Advanced machine learning based attribution is outside the current scope but can be added in future versions.

## Future Improvements

Future improvements may include:

Live connection to advertising APIs
Automated scheduled data refresh
Machine learning based attribution
Customer segmentation
Predictive budget allocation
Streamlit dashboard deployment
More advanced Power BI drill through pages
Campaign recommendation engine

## Conclusion

The Multi Touch Marketing Attribution and ROI Analytics Dashboard provides a strong analytical foundation for measuring marketing effectiveness. It improves on simple last click reporting by showing how different channels contribute to conversions under multiple attribution models.

The project combines Python, SQL, PostgreSQL, testing and dashboard visualization to produce a practical business intelligence solution. It can support better marketing decisions, improved budget allocation and clearer understanding of customer journeys.
