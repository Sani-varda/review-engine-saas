import requests
import json
import os
import time

# Notion Config
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DB_USA = "31bd4166da0580d69fb5d89b90f38e79"
DB_INDIA = "31bd4166da058074ba49ffb9233e6ed6"

# Resend Integration
from send_resend_email import send_sales_email

def get_leads_to_email(database_id):
    """Fetch leads from Notion that have an email but haven't been contacted."""
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    # Filter: Email is NOT empty AND Outreach Status IS 'Ready'
    payload = {
        "filter": {
            "and": [
                { "property": "Email Address", "email": { "is_not_empty": True } },
                { "property": "Outreach Status", "select": { "equals": "Ready" } }
            ]
        }
    }
    
    try:
        res = requests.post(f"https://api.notion.com/v1/databases/{database_id}/query", headers=headers, json=payload)
        if res.ok:
            return res.json().get("results", [])
    except Exception as e:
        print(f"Error fetching leads: {e}")
    return []

def update_notion_status(page_id, status="Contacted"):
    """Update lead status in Notion after sending email."""
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    payload = {
        "properties": {
            "Outreach Status": { "select": { "name": status } }
        }
    }
    requests.patch(f"https://api.notion.com/v1/pages/{page_id}", headers=headers, json=payload)

def main():
    print("🚀 Starting Marcus (Marketing Sub-Agent) Outreach Cycle...")
    
    for db_id in [DB_USA, DB_INDIA]:
        leads = get_leads_to_email(db_id)
        print(f"Found {len(leads)} leads ready for outreach in DB: {db_id}")
        
        for page in leads:
            props = page["properties"]
            email = props["Email Address"]["email"]
            name = props["Name"]["title"][0]["text"]["content"]
            
            # Determine pain point for the email template
            website = props.get("Website", {}).get("url")
            pain_point = "missing website" if not website else "low reviews"
            
            print(f"📧 Sending professional ROI email to: {name} ({email})...")
            
            # Trigger Marcus's Email Engine
            success = send_sales_email(email, name, pain_point)
            
            if success:
                update_notion_status(page["id"])
                print(f"✅ Success. Status updated in Notion.")
            
            # Anti-spam delay
            time.sleep(2)

if __name__ == "__main__":
    main()
