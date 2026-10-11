import json
import requests

# Replace with a valid Zoho OAuth access token
# Generate via: https://api-console.zoho.com → Self Client → Scope: ZohoBooks.fullaccess.all
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN_HERE"

def runner(context, basicIO):
    moduleObject = json.loads(basicIO.getParameter("invoice"))
    context.log.INFO(moduleObject)

    organizationObject = json.loads(basicIO.getParameter("organization"))
    organization_id = organizationObject["organization_id"]
    context.log.INFO("Organization ID " + organization_id)

    invoice_id = moduleObject["invoice_id"]
    api_root = organizationObject["api_root_endpoint"]

    headers = {
        "Authorization": "Zoho-oauthtoken " + ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    # Step 2: Fetch invoice to get salesorder_id
    invoice_url = api_root + "/invoices/" + invoice_id + "?organization_id=" + organization_id
    invoice_resp = requests.get(invoice_url, headers=headers)
    invoice_data = invoice_resp.json().get("invoice", {})
    salesorder_id = invoice_data.get("salesorder_id", "")
    context.log.INFO("Sales Order ID: " + str(salesorder_id))

    if not salesorder_id:
        context.log.INFO("No Sales Order linked to this invoice.")
        return

    # Step 3: Fetch SO comments to find linked PO
    comments_url = api_root + "/salesorders/" + salesorder_id + "/comments?organization_id=" + organization_id
    comments_resp = requests.get(comments_url, headers=headers)
    comments = comments_resp.json().get("comments", [])

    purchase_order_id = None
    for comment in comments:
        if comment.get("transaction_type", "").lower() == "purchaseorder":
            purchase_order_id = comment.get("transaction_id")
            break

    if not purchase_order_id:
        context.log.INFO("No Purchase Order linked to this Sales Order.")
        return

    context.log.INFO("Purchase Order ID: " + str(purchase_order_id))

    # Step 4: Fetch PO number
    po_url = api_root + "/purchaseorders/" + purchase_order_id + "?organization_id=" + organization_id
    po_resp = requests.get(po_url, headers=headers)
    po_data = po_resp.json().get("purchaseorder", {})
    po_number = po_data.get("purchaseorder_number", "")
    context.log.INFO("PO Number: " + str(po_number))

    # Step 5: Update invoice custom field with PO number
    update_url = api_root + "/invoices/" + invoice_id + "?organization_id=" + organization_id
    payload = {
        "custom_fields": [
            {
                "api_name": "cf_cf_po_num",
                "value": po_number
            }
        ]
    }
    update_resp = requests.put(update_url, headers=headers, json=payload)
    result = update_resp.json()
    context.log.INFO("Update result: " + str(result.get("message", "")))
