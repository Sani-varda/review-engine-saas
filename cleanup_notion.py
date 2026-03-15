import requests
import json
import os

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = "31bd4166da0580d69fb5d89b90f38e79"
TARGET_NAME = "Mann Family Dental"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def main():
    print(f"Querying for '{TARGET_NAME}'...")
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {"filter": {"property": "Name", "title": {"equals": TARGET_NAME}}}
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Error: {response.text}")
        return

    pages = response.json().get("results", [])
    if not pages:
        print("No matches.")
        return

    print(f"Found {len(pages)} matches.")
    
    # Keep oldest (earliest created_time)
    pages.sort(key=lambda x: x["created_time"])
    
    keep = pages[0]
    to_archive = pages[1:]
    
    print(f"Keeping oldest: {keep['id']}")
    
    removed_count = 0
    for page in to_archive:
        print(f"Archiving {page['id']}...")
        url_p = f"https://api.notion.com/v1/pages/{page['id']}"
        res_p = requests.patch(url_p, headers=headers, json={"archived": True})
        if res_p.status_code == 200:
            removed_count += 1
        else:
            print(f"Failed to archive {page['id']}: {res_p.text}")

    print(f"DONE. Removed {removed_count} duplicates.")

if __name__ == "__main__":
    main()
