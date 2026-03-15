import os
import httpx
from typing import Optional

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def generate_review_reply(review_text: str, business_name: str, star_rating: int) -> Optional[str]:
    """
    Generates an empathetic and professional reply to a customer review using Gemini 2 Flash.
    """
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY not set. Skipping AI generation.")
        return None

    prompt = f"""
    You are the manager of {business_name}. A customer left a {star_rating}-star review with the following comment:
    "{review_text}"
    
    Please write a professional, warm, and concise reply. 
    If the review is positive (4-5 stars), express gratitude and invite them back.
    If the review is negative (1-3 stars), apologize, express empathy, and invite them to reach out privately to resolve any issues.
    
    Keep the reply under 3 sentences.
    """

    # Using Gemini 2 Flash for speed and cost efficiency
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2-flash:generateContent?key={GEMINI_API_KEY}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10.0)
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text'].strip()
            else:
                print(f"Gemini API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error generating AI reply: {e}")
    
    return None
