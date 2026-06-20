# Dataset Analysis

## Ad Spend Dataset

### Columns
- Campaign_id
- Channel
- Spend
- Clicks
- Impressions
- Date

### Purpose
Stores campaign marketing spend and performance metrics.

### Possible Primary Key
Campaign_id + Date

---

## Customer Interaction Dataset

### Columns
- Campaign_id
- Channel
- Spend
- Clicks
- Impressions
- Date

### Purpose
Stores campaign interaction information.

### Possible Primary Key
Campaign_id + Date

---

## Revenue Dataset

### Columns
- Conversion_id
- User_id
- Revenue
- Conversion_date

### Purpose
Stores revenue generated from customer conversions.

### Possible Primary Key
Conversion_id

---

## Dataset Relationship Analysis

Ad Spend ↔ Interaction:
Possible Join Key:
- Campaign_id
- Date

Interaction ↔ Revenue:
UNKNOWN

Revenue ↔ Ad Spend:
UNKNOWN

---

## Risk

Currently no visible common key exists between
Revenue Dataset and Marketing Datasets.

Further investigation required.