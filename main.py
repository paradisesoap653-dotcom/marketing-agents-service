import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

# إعداد مفتاح API المباشر لـ Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

app = FastAPI(title="Marketing Service")

class CampaignRequest(BaseModel):
    product_name: str
    target_audience: str

@app.get("/")
def home():
    return {"status": "Service is running perfectly!"}

@app.post("/run-campaign")
def run_campaign(request: CampaignRequest):
    try:
        # استخدام الموديل المباشر والسريع
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        أنت خبير تسويق رقمي محترف. 
        قم بكتابة منشور تسويقي مبتكر وجذاب لمنتج: {request.product_name}
        الجمهور المستهدف: {request.target_audience}
        شامل الهاشتاجات المناسبة.
        """
        
        response = model.generate_content(prompt)
        
        return {
            "success": True, 
            "result": response.text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
