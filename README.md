# Zoho Books — Purchase Order Auto-Reference on Invoice

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Zoho Books](https://img.shields.io/badge/Zoho-Books%20API%20v3-red)
![OAuth2](https://img.shields.io/badge/Auth-OAuth2-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

A Python automation deployed as a **Zoho Books Custom Function** that automatically fetches and stamps the associated **Purchase Order (PO) number** onto an Invoice via a custom field — triggered by a Workflow Rule every time an Invoice is created.

---

## Problem Statement

In Zoho Books, when a **Sales Order** is converted to an **Invoice**, the Sales Order number is reflected on the Invoice automatically. However, if a **Purchase Order** was raised from that Sales Order, the PO number is **not displayed** on the Invoice — even though it is a critical reference for the customer and the finance team.

This is a known gap in Zoho Books with no native solution.

---

## Solution

This script is deployed inside Zoho Books as a **Python Custom Function** and wired to a **Workflow Rule** (trigger: Invoice Created). It automatically:

1. Extracts the Invoice ID and Organization ID from the trigger payload
2. Fetches the Invoice details to identify the linked Sales Order
3. Scans the Sales Order's comment history to locate the associated Purchase Order
4. Retrieves the Purchase Order number via the Zoho Books API
5. Updates the Invoice with the PO number in a dedicated custom field

---

## Workflow

Customer Order Received
↓
Sales Order Created (SO-XXXXX)
↓
Purchase Order Raised from Sales Order (PO-XXXXX)
↓
Sales Order Converted to Invoice (INV-XXXXX)
↓
Workflow Rule Fires → Custom Function Triggered
↓
PO Number Auto-Stamped on Invoice (cf_PO_num field)


---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python |
| API | Zoho Books REST API v3 |
| Authentication | OAuth2 (Self Client / Access Token) |
| HTTP Client | `requests` |
| Deployment | Zoho Books Custom Function (In-App Editor) |
| Trigger | Zoho Books Workflow Rule |

---

## Project Structure

zoho-po-ref-on-invoice/
│
├── po_ref_on_inv.py # Main custom function script
├── .gitignore # Ignores secrets and cache files
└── README.md # Project documentation


---

## Setup & Deployment

### Prerequisites
- Active Zoho Books account
- Access to Settings → Automation
- Zoho API Console access at https://api-console.zoho.com

---

### Step 1 — Create a Custom Field on Invoices

1. Go to **Settings → Sales → Invoices → Fields**
2. Click **+ New Custom Field**
3. Label: `cf_PO_num` | Type: Text Box (Single Line)
4. Enable **Show in All PDFs**
5. Save and note the **API Field Name** (e.g. `cf_cf_po_num`)

---

### Step 2 — Generate an OAuth Access Token

1. Go to [https://api-console.zoho.com](https://api-console.zoho.com)
2. Click **Self Client → Generate Code**
3. Scope: `ZohoBooks.fullaccess.all`
4. Copy the grant code and run:

```bash
curl -X POST "https://accounts.zoho.com/oauth/v2/token" \
  -d "grant_type=authorization_code" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "code=YOUR_GRANT_CODE" \
  -d "redirect_uri=https://www.zoho.com"
```

5. Copy the `access_token` from the JSON response

---

### Step 3 — Deploy the Custom Function

1. Go to **Settings → Automation → Workflow Actions → Custom Functions**
2. Click **+ New Custom Function**
3. Function Name: `po_ref_on_inv` | Module: **Invoice** | Language: **Python**
4. Paste the contents of `po_ref_on_inv.py`
5. Replace `YOUR_ACCESS_TOKEN_HERE` with your actual access token
6. Replace `cf_cf_po_num` with your actual custom field API name if different
7. Click **Save**

---

### Step 4 — Create a Workflow Rule

1. Go to **Settings → Automation → Workflow Rules**
2. Click **+ New Rule**
3. Module: **Invoice** | Trigger: **When an Invoice is Created**
4. No criteria needed — applies to all invoices
5. Under **Immediate Actions** → Add → **Custom Function** → select `po_ref_on_inv`
6. Click **Associate** → **Save**

---

## Output

Once deployed, every Invoice created from a Sales Order with a linked Purchase Order will automatically show:

| Field | Value |
|-------|-------|
| Invoice # | INV-000017 |
| Order Number | SO-00004 |
| cf_PO_num | **PO-00003** ← auto-stamped |

---

## Key Learnings

- Zoho Books REST API v3 structure and authentication
- OAuth2 Self Client token generation and usage
- Tracing relational data across SO → PO → Invoice via comment history
- Deploying Python scripts inside Zoho's custom function runtime
- Workflow Rule automation for business process triggers

---

## Author

**Raghav Balaji V**  
Aspiring Data Analyst | Python | SQL | Power BI | ML  
[GitHub](https://github.com/raghav-010) · [LinkedIn](https://linkedin.com/in/raghavbalaji010)
