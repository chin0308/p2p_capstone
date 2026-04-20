# 📦 SAP Procure-to-Pay (P2P) Analytics Dashboard

### End-to-End Procure-to-Pay Process with Data Analytics Insights
#### Capstone Project — NexCore Manufacturing Pvt Ltd

---

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.0+-green?logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-lightblue?logo=pandas&logoColor=white)
![SAP](https://img.shields.io/badge/SAP-S%2F4HANA-blue?logo=sap&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🌐 Project Overview

This capstone project models the complete **SAP Procure-to-Pay (P2P) business process** for a fictitious manufacturing company — **NexCore Manufacturing Pvt Ltd** — and pairs it with a fully functional **Streamlit analytics dashboard** that provides real-time procurement insights.

The project bridges the gap between enterprise ERP concepts (SAP MM/FI modules) and modern data analytics by:

- Mapping every P2P step to real SAP T-codes and document flows
- Simulating realistic procurement transaction data (120 records, 19 fields)
- Delivering an interactive dashboard with KPIs, spend trends, vendor scoring, delay analysis, and payment tracking

---

## 🏢 Company Details

| Field | Details |
|---|---|
| Company | NexCore Manufacturing Pvt Ltd |
| Industry | Industrial Manufacturing |
| HQ | Pune, Maharashtra, India |
| ERP | SAP S/4HANA |
| Currency | INR |
| Plants | PLANT01 (Pune), PLANT02 (Nashik), PLANT03 (Hyderabad) |

---

## 🗂️ Project Structure

```
p2p-capstone/
│
├── 📂 data/
│   ├── p2p_dataset.csv          # 120-row realistic P2P transaction dataset
│   └── generate_data.py         # Script used to generate the dataset
│
├── 📂 app/
│   └── app.py                   # Streamlit dashboard (main application)
│
├── 📂 docs/
│   ├── project_documentation.md # Full 5-page project documentation
│   └── viva_prep.md             # 10 viva Q&As + SAP concept cheat sheet
│
├── 📂 screenshots/
│   └── README.md                # Screenshot descriptions & capture guide
│
├── README.md                    # This file
└── requirements.txt             # Python dependencies
```

---

## ✨ Features

### 📊 Dashboard Features

| Feature | Description |
|---|---|
| **6 KPI Cards** | Total Spend, PO Count, Avg Delay, Top Vendor, Pending, Overdue |
| **Monthly Trend** | Interactive area chart of procurement spend by month |
| **Material Analysis** | Horizontal bar chart ranking materials by spend |
| **Quarterly View** | Donut chart showing spend by quarter |
| **Vendor Performance** | Bar chart + bubble scatter (PO count vs delay vs spend) |
| **Vendor Scorecard** | Risk classification (🟢 Low / 🟡 Medium / 🔴 High) |
| **Delay Histogram** | Distribution of delivery delays across all orders |
| **On-Time Analysis** | Donut chart: on-time vs delayed deliveries |
| **Payment Tracking** | Paid / Pending / Overdue breakdown by vendor |
| **Raw Data Table** | Searchable, filterable data with CSV export |
| **Dynamic Filters** | Vendor, Plant, Payment Status, Date Range |
| **File Upload** | Load your own P2P CSV dataset |

### 📋 SAP P2P Documentation

- Step-by-step mapping of all 7 P2P stages
- Real SAP T-codes for every step
- Key SAP tables (EKKO, EKPO, MSEG, RBKP, etc.)
- Three-way match explanation with accounting entries
- GR/IR clearing account mechanics
- Complete viva preparation with 10 Q&As

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip package manager
- Git (optional, for cloning)

### Step 1 — Clone the Repository

```bash
git clone https://github.com/yourusername/p2p-capstone.git
cd p2p-capstone
```

### Step 2 — Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Run the Dashboard

```bash
streamlit run app/app.py
```

The app will open automatically in your browser at:
```
http://localhost:8501
```

### Step 5 — (Optional) Regenerate Dataset

```bash
python data/generate_data.py
```

---

## 📸 Dashboard Screenshots

### KPI Overview
> Six real-time metric cards showing Total Spend, PO Count, Avg Delay, Top Vendor, Pending and Overdue Invoices. Updates dynamically with sidebar filters.

### Monthly Spend Trend
> Interactive area chart with hover tooltips. Reveals procurement seasonality and peak spending months across the fiscal year.

### Vendor Performance
> Side-by-side: bar chart for spend ranking + bubble scatter plot mapping PO volume, delivery reliability, and total spend in one view.

### Delivery Delay Analysis
> Histogram + monthly trend line with reference average + on-time vs delayed donut + top delayed materials bar chart.

### Payment Status
> Donut chart (Paid/Pending/Overdue) + stacked vendor bar + overdue spend highlighted in red for immediate action.

*(Run the app and capture screenshots from each tab — see `/screenshots/README.md` for guidance)*

---

## 📊 Dataset Details

**File:** `data/p2p_dataset.csv`  
**Rows:** 120 transactions  
**Period:** Jan 2023 – Dec 2023

| Column | Description |
|---|---|
| PO_ID | Unique Purchase Order ID |
| PR_ID | Source Purchase Requisition ID |
| Vendor_ID | Vendor code (V001–V010) |
| Vendor_Name | Full vendor name |
| Material | Material/product procured |
| Plant | Receiving plant (PLANT01-03) |
| Storage_Loc | Storage location within plant |
| Purchasing_Org | Purchasing organization |
| Order_Date | PO creation date |
| Delivery_Date | Actual delivery date |
| GR_Date | Goods Receipt posting date |
| Invoice_Date | Invoice received date |
| Quantity | Ordered quantity |
| Unit_Price | Price per unit (INR) |
| Total_Amount | Total order value (INR) |
| Currency | Transaction currency |
| Payment_Status | Paid / Pending / Overdue |
| Delay_Days | Days beyond standard lead time |
| Payment_Terms | Net 30 / Net 45 / Net 60 |

---

## 🗺️ SAP P2P Process Map

| Step | T-Code | Document | Output |
|---|---|---|---|
| 1. Purchase Requisition | ME51N | PR Document | Approved internal request |
| 2. Request for Quotation | ME41 / ME49 | RFQ | Vendor selected |
| 3. Purchase Order | ME21N | PO Document | Legal order sent to vendor |
| 4. Goods Receipt | MIGO (Mvt 101) | Material Doc | Stock updated |
| 5. Invoice Verification | MIRO | Invoice Doc | 3-way match verified |
| 6. Payment Run | F110 | Payment Doc | Vendor paid |
| 7. Reconciliation | FBL1N | Reports | Accounts cleared |

---

## 🛠️ Technology Stack

| Category | Tool | Version |
|---|---|---|
| Web Framework | Streamlit | ≥ 1.32 |
| Data Processing | Pandas | ≥ 2.0 |
| Visualization | Plotly Express | ≥ 5.0 |
| Language | Python | ≥ 3.10 |
| ERP Concept | SAP S/4HANA | — |
| Docs | Markdown | — |
| Version Control | Git + GitHub | — |

---

## 📄 Documentation

| Document | Location | Description |
|---|---|---|
| Project Documentation | `docs/project_documentation.md` | Full 5-page academic report |
| Viva Preparation | `docs/viva_prep.md` | 10 Q&As + SAP cheat sheet |
| Screenshots Guide | `screenshots/README.md` | Screenshot descriptions |
| This README | `README.md` | Project overview and setup |

---

## 🎓 Academic Context

This project was developed as a capstone submission covering:

- **Enterprise Resource Planning (ERP)** — SAP MM and FI-AP modules
- **Business Process Management** — P2P lifecycle mapping
- **Data Analytics** — KPI design, visualization, trend analysis
- **Full-Stack Development** — Python, Streamlit, Plotly

**Key learning outcomes:**
1. Understanding SAP organizational structures and master data
2. Mapping business processes to SAP T-codes and document flows
3. Simulating SAP data extraction for analytics
4. Building production-grade dashboards for business decision support

---

## 📬 Contact

For questions about this project:

- **Project Team:** Capstone Group [Your Name / Team]
- **Institution:** [Your Institution Name]
- **Department:** [Your Department]
- **Guide/Mentor:** [Mentor Name]

---

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ using Streamlit · Pandas · Plotly &nbsp;|&nbsp; SAP P2P Capstone Project
</p>
