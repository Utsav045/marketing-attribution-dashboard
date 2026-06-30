# Database Design

## Overview

The Marketing Attribution Dashboard uses a PostgreSQL database to store customer interactions, campaign information, conversion events, and revenue data. The database is designed to support attribution analysis, KPI calculations, and dashboard reporting.

---

# Database Tables

## 1. Campaigns

**Purpose:**
Stores information about marketing campaigns.

| Column        | Data Type     | Description       |
| ------------- | ------------- | ----------------- |
| campaign_id   | SERIAL        | Primary Key       |
| campaign_name | VARCHAR(100)  | Campaign name     |
| channel       | VARCHAR(50)   | Marketing channel |
| spend         | DECIMAL(12,2) | Campaign cost     |

---

## 2. Customers

**Purpose:**
Stores customer information.

| Column        | Data Type    | Description   |
| ------------- | ------------ | ------------- |
| customer_id   | SERIAL       | Primary Key   |
| customer_name | VARCHAR(100) | Customer name |
| email         | VARCHAR(100) | Email address |

---

## 3. Customer_Journeys

**Purpose:**
Stores customer interactions before conversion.

| Column           | Data Type     | Description         |
| ---------------- | ------------- | ------------------- |
| journey_id       | SERIAL        | Primary Key         |
| customer_id      | INTEGER       | Foreign Key         |
| campaign_id      | INTEGER       | Foreign Key         |
| interaction_date | DATE          | Interaction date    |
| touch_order      | INTEGER       | Touchpoint sequence |
| converted        | BOOLEAN       | Conversion status   |
| revenue          | DECIMAL(12,2) | Revenue generated   |

---

# Relationships

* One customer can have multiple customer journey records.
* One campaign can interact with multiple customers.
* Customer journeys link customers and campaigns using foreign keys.

---

# Database Objectives

* Store marketing campaign information.
* Track customer journeys.
* Support attribution model calculations.
* Calculate marketing KPIs.
* Provide structured data for dashboard visualization.

---

# Indexing Strategy

The following indexes improve query performance:

* Index on `customer_id`
* Index on `campaign_id`
* Index on `interaction_date`

---

# Future Enhancements

* Add user authentication tables.
* Store attribution results.
* Implement audit logging.
* Optimize database for large-scale analytics.