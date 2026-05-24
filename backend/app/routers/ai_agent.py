from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class CustomerData(BaseModel):
    name: str
    status: str

@router.post("/draft-email")
async def draft_email(data: CustomerData):
    try:
        import google.generativeai as genai
        GOOGLE_API_KEY = "AIzaSyAQMt5aTWgYz8T1m_vRcqCNPY6ymS7CgO8"
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Write a short, professional 2-line sales follow-up email for a customer named '{data.name}' whose current status is '{data.status}'. Only return the email body, no subject line."
        response = model.generate_content(prompt)
        return {"email": response.text}
    except Exception as e:
        print("AI Fallback Triggered:", e)
        fallback_email = f"Hi {data.name} Team,\n\nI'm following up regarding our recent discussions. Since your current status is '{data.status}', I wanted to see if there's anything else you need from our end to move forward.\n\nBest regards,\nHosho Sales Team"
        return {"email": fallback_email}
