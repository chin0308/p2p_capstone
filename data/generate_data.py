import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

vendors = [
    ("V001", "TechSupply India Pvt Ltd"),
    ("V002", "Global Office Essentials"),
    ("V003", "SteelCraft Industries"),
    ("V004", "RawMat Solutions"),
    ("V005", "BrightPack Logistics"),
    ("V006", "ProChem Supplies"),
    ("V007", "AgroFresh Vendors"),
    ("V008", "MechaParts Co."),
    ("V009", "SafeWear Equipment"),
    ("V010", "DataPrint Technologies"),
]

materials = [
    ("Laptop",            45000, 60000),
    ("Office Chair",       8000, 15000),
    ("Steel Sheets",       5000,  9000),
    ("Raw Polymer",        3000,  7000),
    ("Packaging Material", 1500,  4000),
    ("Chemical Solvent",   2500,  6000),
    ("Organic Fertilizer", 1000,  3000),
    ("Gear Assembly",      7000, 12000),
    ("Safety Helmet",       800,  2000),
    ("Printer Cartridge",  1200,  3500),
    ("Server Rack",       80000,120000),
    ("Network Switch",    25000, 40000),
    ("Office Desk",       12000, 20000),
    ("Fire Extinguisher",  3500,  6000),
    ("Conveyor Belt",     30000, 55000),
]

payment_statuses = ["Paid", "Paid", "Paid", "Pending", "Overdue"]

rows = []
start_date = datetime(2023, 1, 1)

for i in range(1, 121):
    vendor = random.choice(vendors)
    material = random.choice(materials)

    order_date = start_date + timedelta(days=random.randint(0, 364))
    std_lead    = random.randint(5, 15)
    delay       = random.randint(-2, 20)           # negative = early
    delivery_days = max(1, std_lead + delay)
    delivery_date = order_date + timedelta(days=delivery_days)
    gr_date       = delivery_date + timedelta(days=random.randint(0, 3))
    invoice_date  = gr_date       + timedelta(days=random.randint(1, 7))

    quantity    = random.randint(1, 50)
    unit_price  = round(random.uniform(material[2] * 0.9, material[2]), 2)
    total       = round(quantity * unit_price, 2)
    delay_days  = max(0, delivery_days - std_lead)
    pay_status  = random.choice(payment_statuses)

    rows.append({
        "PO_ID":          f"PO{str(i).zfill(4)}",
        "PR_ID":          f"PR{str(i).zfill(4)}",
        "Vendor_ID":      vendor[0],
        "Vendor_Name":    vendor[1],
        "Material":       material[0],
        "Plant":          random.choice(["PLANT01", "PLANT02", "PLANT03"]),
        "Storage_Loc":    random.choice(["SL01", "SL02", "SL03"]),
        "Purchasing_Org": "PO_ORG_IN",
        "Order_Date":     order_date.strftime("%Y-%m-%d"),
        "Delivery_Date":  delivery_date.strftime("%Y-%m-%d"),
        "GR_Date":        gr_date.strftime("%Y-%m-%d"),
        "Invoice_Date":   invoice_date.strftime("%Y-%m-%d"),
        "Quantity":       quantity,
        "Unit_Price":     unit_price,
        "Total_Amount":   total,
        "Currency":       "INR",
        "Payment_Status": pay_status,
        "Delay_Days":     delay_days,
        "Payment_Terms":  random.choice(["Net 30", "Net 45", "Net 60"]),
    })

df = pd.DataFrame(rows)
df.to_csv("/home/claude/p2p-capstone/data/p2p_dataset.csv", index=False)
print(f"Dataset created: {len(df)} rows")
print(df.head(3))
