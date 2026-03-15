import requests
import time

# Configuration
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = "31bd4166da0580d69fb5d89b90f38e79"
TARGET_NAME = "Mann Family Dental"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def query_duplicates():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {
        "filter": {
            "property": "Name",
            "title": {
                "equals": TARGET_NAME
            }
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Error querying database: {response.text}")
        return []
    
    return response.json().get("results", [])

def archive_page(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"archived": True}
    response = requests.patch(url, headers=headers, json=payload)
    return response.status_code == 200

def main():
    pages = query_duplicates()
    if not pages:
        print("No entries found.")
        return

    print(f"Found {len(pages)} entries.")
    
    # Sort by created_time (oldest first)
    pages.sort(key=lambda x: x["created_time"])
    
    keep_page = pages[0]
    to_delete = pages[1:]
    
    print(f"Keeping oldest entry: {keep_page['id']} (Created: {keep_page['created_time']})")
    
    removed_count = 0
    for page in to_delete:
        print(f"Archiving duplicate: {page['id']} (Created: {page['created_time']})")
        if archive_page(page["id"]):
            removed_count += 1
            # Brief sleep to avoid hitting rate limits too hard during bulk delete
            time.sleep(0.3)
        else:
            print(f"Failed to archive {page['id']}")
            
    print(f"Cleanup complete. Removed {removed_count} duplicates.")

if __name__ == "__main__":
    main()
