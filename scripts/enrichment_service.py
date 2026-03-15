import os
import requests
import json
import re
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")

class EnrichmentService:
    def __init__(self):
        self.tavily_url = "https://api.tavily.com/search"
        self.apollo_base_url = "https://api.apollo.io/v1"

    def apollo_search(self, company_name: str) -> Dict:
        """Use Apollo.io to find top decision makers using the organization search endpoint."""
        if not APOLLO_API_KEY:
            return {}
        
        headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "X-Api-Key": APOLLO_API_KEY
        }
        
        try:
            # Using the People Search endpoint directly with company name
            payload = {
                "q_organization_name": company_name,
                "person_titles": ["Owner", "Founder", "Manager", "CEO", "Veterinarian", "Dentist"],
                "display_mode": "explorer"
            }
            
            res = requests.post(f"{self.apollo_base_url}/mixed_people/search", json=payload, headers=headers)
            
            if res.status_code == 200:
                people = res.json().get("people", [])
                if people:
                    person = people[0]
                    return {
                        "name": person.get("name"),
                        "title": person.get("title"),
                        "email": person.get("email"),
                        "linkedin": person.get("linkedin_url")
                    }
        except Exception as e:
            print(f"    ⚠️ Apollo People Search error: {e}")
        return {}

    def search_tavily(self, query: str) -> str:
        if not TAVILY_API_KEY:
            return ""
        payload = {"api_key": TAVILY_API_KEY, "query": query, "search_depth": "advanced"}
        try:
            res = requests.post(self.tavily_url, json=payload)
            if res.status_code == 200:
                results = res.json().get("results", [])
                return "\n\n".join([f"Source: {r['url']}\nContent: {r['content']}" for r in results])
        except Exception as e:
            print(f"    ❌ Tavily search failed: {e}")
        return ""

    def enrich_leads(self, leads: List[Dict]) -> List[Dict]:
        """Hybrid Enrichment: Apollo.io + Tavily Search."""
        enriched_leads = []
        for lead in leads:
            print(f"  🔍 Investigating: {lead['name']}...")
            
            lead["contact_name"] = lead.get("contact_name", "Unknown")
            lead["contact_email"] = lead.get("contact_email", None)
            lead["linkedin_url"] = lead.get("linkedin_url", None)
            lead["instagram_url"] = lead.get("instagram_url", None)
            
            # Phase 1: Apollo.io (Premium Contact Data)
            apollo_data = self.apollo_search(lead["name"])
            if apollo_data:
                lead["contact_name"] = apollo_data.get("name", "Unknown")
                lead["contact_email"] = apollo_data.get("email")
                lead["linkedin_url"] = apollo_data.get("linkedin")
                print(f"    🧬 Apollo Found: {lead['contact_name']}")

            # Phase 2: Tavily (Scraping Supplement for Socials)
            query = (
                f"Official LinkedIn and Instagram for "
                f"'{lead['name']}' in {lead.get('location', 'USA')}. "
            )
            search_context = self.search_tavily(query)
            
            if search_context:
                # 1. Extract Email if Apollo missed it
                if not lead.get("contact_email"):
                    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', search_context)
                    filtered = [e for e in emails if not any(j in e.lower() for j in ["example", "domain", "sentry"])]
                    if filtered:
                        lead["contact_email"] = filtered[0]
                        print(f"    📧 Tavily Found Email: {lead['contact_email']}")

                # 2. Extract Socials
                if not lead.get("linkedin_url"):
                    li = re.findall(r'https?://(?:www\.)?linkedin\.com/(?:company|in)/[a-zA-Z0-9_-]+', search_context)
                    if li: 
                        lead["linkedin_url"] = li[0]
                        print(f"    💼 Tavily Found LinkedIn: {lead['linkedin_url']}")

                if not lead.get("instagram_url"):
                    ig = re.findall(r'https?://(?:www\.)?instagram\.com/[a-zA-Z0-9._-]+', search_context)
                    if ig: 
                        lead["instagram_url"] = ig[0]
                        print(f"    📸 Tavily Found Instagram: {lead['instagram_url']}")

            enriched_leads.append(lead)
        return enriched_leads

enricher = EnrichmentService()
