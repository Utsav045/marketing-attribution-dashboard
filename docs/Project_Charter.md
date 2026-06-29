# Marketing Attribution Dashboard Project Charter

## Project Title

Multi Touch Marketing Attribution and ROI Analytics Dashboard

## Project Type

Data Analytics, Business Intelligence and Marketing Performance Analytics Project

## Project Duration

4 Weeks

## Project Repository

marketing-attribution-dashboard

## Project Background

Modern businesses spend money across several digital marketing channels such as Google Ads, Facebook, Instagram, LinkedIn, YouTube, Email and organic content. A customer may interact with many of these channels before finally making a purchase. Traditional last click attribution gives all conversion credit to the final interaction, even when earlier channels helped create awareness and interest.

This creates a business problem because marketing teams may wrongly believe that only the final channel contributed to revenue. As a result, companies can waste money on weak campaigns while reducing budget for channels that actually support customer acquisition.

This project solves that problem by building a marketing attribution analytics system that tracks customer journeys, cleans marketing datasets, calculates attribution credit and produces useful ROI insights for dashboard reporting.

## Problem Statement

Marketing teams need a better way to understand how different channels contribute to conversions and revenue. The existing approach of using only last click attribution does not fairly distribute credit across the customer journey. This can lead to poor budget allocation, wrong ROI calculation, inaccurate CAC reporting and weak campaign optimization.

The project therefore focuses on building an analytics workflow that supports first touch, last touch, linear, time decay and position based attribution models. The final output will help users compare channel performance, calculate KPIs and make better marketing decisions.

## Project Aim

The aim of this project is to develop a multi touch marketing attribution and ROI dashboard that can ingest marketing data, clean the data, construct customer journeys, apply attribution models, calculate performance KPIs and support visual business reporting.

## Project Objectives

The objectives of the project are to:

1. Ingest raw marketing datasets including ad spend, customer interactions and conversions.
2. Clean and standardize the raw datasets for analysis.
3. Build customer journey paths from interaction history.
4. Design a database structure for storing clean marketing analytics data.
5. Develop SQL queries for journey sequencing, attribution logic and KPI calculations.
6. Implement first touch, last touch, linear, time decay and position based attribution models.
7. Calculate marketing KPIs such as spend, revenue, CPC, CPM, CAC, ROAS and ROI.
8. Create reporting views for dashboard visualization.
9. Validate the accuracy of attribution weights and revenue allocation.
10. Produce documentation that explains the workflow, logic and business value of the project.

## Scope of the Project

The scope of this project covers data ingestion, data cleaning, customer journey construction, attribution modeling, SQL database design, KPI engineering, dashboard preparation and project documentation.

The project does not focus on live advertising API connection at this stage. The system is designed to work with available marketing datasets and can later be extended to real time API pipelines.

## Datasets

The project uses three main categories of datasets:

### Ad Spend Dataset

This contains campaign level marketing cost data.

Expected fields include:

campaign_id
channel
spend
clicks
impressions
date

### Customer Journey Dataset

This contains user interaction records across marketing channels.

Expected fields include:

user_id
channel
interaction_time
campaign_id

### Conversion Dataset

This contains customer conversion and revenue records.

Expected fields include:

conversion_id
user_id
revenue
conversion_date

## Team Members and Responsibilities

### Utsav

Team Lead, architecture, integration and pipeline orchestration.

### Rajarshi

Python development, data processing, analytics and visualization support.

### Isaac

SQL development, database design, advanced SQL logic, attribution queries, KPI calculations, trend analysis and query optimization.

### Palak

Documentation, testing support, dataset research and presentation preparation.

## Isaac's Responsibility

Isaac is responsible for the database and SQL layer of the project. This includes:

Database schema design
Staging table design
Star schema design
Customer journey sequencing
SQL attribution logic
Monthly and weekly trend analysis
Time decay attribution
Position based attribution
Stored procedures
Dashboard reporting views
KPI calculation queries
SQL validation tests
Database documentation

## Tools and Technologies

Python
Pandas
NumPy
PostgreSQL
SQL
Power BI
Git
GitHub
VS Code
Jupyter Notebook
Pytest

## Attribution Models

### First Touch Attribution

First touch attribution assigns full conversion credit to the first marketing channel that interacted with the customer.

### Last Touch Attribution

Last touch attribution assigns full conversion credit to the final marketing channel before conversion.

### Linear Attribution

Linear attribution distributes conversion credit equally across all customer touchpoints before conversion.

### Time Decay Attribution

Time decay attribution gives more credit to touchpoints that occur closer to the conversion date.

### Position Based Attribution

Position based attribution gives higher credit to the first and last touchpoints, while the remaining credit is shared among middle touchpoints.

## Key Performance Indicators

The project calculates the following KPIs:

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
Channel Performance
Campaign Performance

## Expected Dashboard Pages

### Executive Overview

This page shows total spend, total revenue, ROAS, ROI, CAC and conversion performance.

### Attribution Analysis

This page compares revenue allocation across first touch, last touch, linear, time decay and position based attribution models.

### Channel Performance

This page shows the performance of each marketing channel using spend, revenue, CAC, ROAS and ROI.

### Trend Analysis

This page shows monthly and weekly marketing performance trends.

### Campaign Insights

This page helps identify high performing and low performing campaigns.

## Expected Business Value

The project will help marketing teams understand which channels contribute most to revenue. It will also help identify wasteful campaigns, improve budget allocation, compare attribution methods and support data driven marketing decisions.

## Deliverables

The final deliverables include:

Cleaned marketing datasets
Python preprocessing scripts
Attribution modeling scripts
PostgreSQL database schema
SQL attribution queries
SQL KPI queries
Advanced reporting views
Validation tests
Power BI dashboard
Project documentation
Final report

## Success Criteria

The project will be considered successful if:

The data pipeline runs successfully.
Customer journeys are correctly constructed.
Attribution models calculate accurate credit allocation.
KPI calculations are correct.
SQL views support dashboard visualization.
Tests pass successfully.
The dashboard clearly explains marketing performance.
GitHub commits show consistent progress.
The project documentation is complete.

## Project Status

The project is in active development. The repository already contains Python modules for ingestion, preprocessing, attribution, analytics, visualization, testing and pipeline execution. Isaac is extending the project by strengthening the SQL and database layer for advanced attribution analysis and dashboard reporting.
