#!/usr/bin/env python3
import os
import requests
import json
import argparse
import random
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

# Config
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")

from enrichment_service import enricher

class JohnHunter:
    """John (The Hunter) - Lead Generation via Google Maps and Multi-Source Enrichment"""

    def __init__(self):
        self.gmaps_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        self.details_url = "https://maps.googleapis.com/maps/api/place/details/json"

    def check_keys(self):
        missing = []
        if not GOOGLE_MAPS_API_KEY: missing.append("GOOGLE_MAPS_API_KEY")
        if missing:
            print(f"❌ Error: Missing API keys in .env: {', '.join(missing)}")
            return False
        return True

    def is_duplicate(self, name: str, database_id: str) -> bool:
        """Check if lead already exists in target Notion database"""
        headers = {
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        payload = {"filter": {"property": "Name", "title": {"equals": name}}}
        try:
            res = requests.post(f"https://api.notion.com/v1/databases/{database_id}/query", json=payload, headers=headers)
            if res.ok:
                return len(res.json().get("results", [])) > 0
        except:
            pass
        return False

    def sweep_google_maps(self, niche: str, location: str, count: int = 20) -> List[Dict]:
        """Find businesses with or without websites (Targeted Leads)"""
        print(f"🔍 Sweeping Google Maps for '{niche}' in '{location}'...")
        params = {"query": f"{niche} in {location}", "key": GOOGLE_MAPS_API_KEY}
        response = requests.get(self.gmaps_url, params=params)
        results = response.json().get("results", [])
        
        leads = []
        for res in results:
            if len(leads) >= count: break
            place_id = res.get("place_id")
            details_params = {
                "place_id": place_id,
                "fields": "name,formatted_address,website,formatted_phone_number,rating,url",
                "key": GOOGLE_MAPS_API_KEY
            }
            details = requests.get(self.details_url, params=details_params).json().get("result", {})
            website = details.get("website")
            
            leads.append({
                "name": details.get("name"),
                "address": details.get("formatted_address"),
                "phone": details.get("formatted_phone_number"),
                "rating": details.get("rating"),
                "maps_url": details.get("url"),
                "website": website,
                "niche": niche,
                "location": location
            })
            print(f"✅ Found Lead: {details.get('name')}")
        return leads

    def push_to_notion(self, leads: List[Dict]):
        """Upload leads to Notion with automatic routing and custom Sales Script"""
        if not NOTION_TOKEN: return
        headers = {
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        DB_INDIA = "31bd4166da058074ba49ffb9233e6ed6"
        DB_USA = "31bd4166da0580d69fb5d89b90f38e79"

        for lead in leads:
            loc = f"{lead.get('address', '')} {lead.get('location', '')}".lower()
            
            # IMPROVED Country Detection
            if any(m in loc for m in ["india", "bangalore", "bengaluru", "hyderabad", "telangana", "karnataka", "mumbai"]):
                target_db = DB_INDIA
                country = "India"
            else:
                target_db = DB_USA
                country = "USA"

            if self.is_duplicate(lead["name"], target_db):
                print(f"  ⏭️ Skipping duplicate: {lead['name']}")
                continue

            # Generate ROI-Focused Sales Script
            business_name = lead["name"]
            website = lead.get("website")
            
            if not website:
                script = (
                    f"Hi, I noticed {business_name} on Google Maps. Your services look excellent, but I couldn't find a website "
                    "for your business. Statistics show that local businesses without a high-converting digital storefront lose "
                    "nearly 40% of potential bookings. I build premium, one-time ownership SaaS websites that function as your "
                    "24/7 sales team. Would you be interested in a brief one-minute demonstration?"
                )
            else:
                script = (
                    f"Hi, I noticed {business_name} on Google Maps. Your services look excellent, but your online review presence "
                    "doesn't quite reflect that quality yet. I have developed a Reputation Engine for MoonLIT Arc that automates "
                    "the process of collecting 5-star reviews on autopilot. Direct social proof like this typically leads to a "
                    "20-30% lift in inquiries. Would you be interested in a brief one-minute demonstration?"
                )

            payload = {
                "parent": {"database_id": target_db},
                "properties": {
                    "Name": {"title": [{"text": {"content": lead["name"]}}]},
                    "Phone Number": {"phone_number": lead["phone"]} if lead.get("phone") else None,
                    "Founder Information": {"rich_text": [{"text": {"content": lead.get("contact_name", "Unknown")}}]},
                    "Google Maps Link": {"url": lead.get("maps_url")} if lead.get("maps_url") else None,
                    "Email Address": {"email": lead.get("contact_email")} if lead.get("contact_email") else None,
                    "City/State": {"rich_text": [{"text": {"content": lead.get("location", "Unknown")}}]},
                    "Country": {"select": {"name": country}},
                    "Outreach Status": {"select": {"name": "New"}},
                    "Sales Script": {"rich_text": [{"text": {"content": script}}]},
                    "Website": {"url": lead["website"]} if lead.get("website") else None,
                    "LinkedIn": {"url": lead.get("linkedin_url")} if lead.get("linkedin_url") else None,
                    "Instagram": {"url": lead.get("instagram_url")} if lead.get("instagram_url") else None
                }
            }
            payload["properties"] = {k: v for k, v in payload["properties"].items() if v is not None}
            requests.post("https://api.notion.com/v1/pages", json=payload, headers=headers)
            print(f"  ☁️ Synced: {lead['name']} to {country} DB")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--niche", type=str, default="high-paying")
    parser.add_argument("--location", type=str, default="Texas")
    parser.add_argument("--count", type=int, default=10)
    args = parser.parse_args()

    NICHES = ["Dental Clinic", "Veterinary Clinic", "Medical Spa", "Hair Clinic", "Salon", "Fitness Studio", "Gym", "Plumbing Services"]
    niche = random.choice(NICHES) if args.niche == "high-paying" else args.niche

    john = JohnHunter()
    if john.check_keys():
        leads = john.sweep_google_maps(niche, args.location, args.count)
        if leads:
            enriched = enricher.enrich_leads(leads)
            john.push_to_notion(enriched)

if __name__ == "__main__":
    main()
