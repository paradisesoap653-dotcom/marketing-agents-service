import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai

# إنشاء الـ Client باستخدام الحزمة الرسمية الجديدة
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

app = FastAPI(title="Marketing Service")

class CampaignRequest(BaseModel):
    product_name: str
    target_audience: str

@app.get("/")
def home():
    return {"status": "Service is running perfectly!"}

@app.post("/run-campaign")
def run_campaign(request: CampaignRequest):
    if not client:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY غير موجود في إعدادات البيئة.")

    try:
        prompt = f"""
        أنت خبير تسويق رقمي محترف. 
        قم بكتابة منشور تسويقي مبتكر وجذاب لمنتج: {request.product_name}
        الجمهور المستهدف: {request.target_audience}
        شامل الهاشتاجات المناسبة.
        """
        
        # استخدام الموديل المستقر المعتمد حالياً gemini-2.0-flash
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
        )
        
        return {
            "success": True, 
            "result": response.text
        }

    except Exception as e:
        print(f"Error details: {e}")
        raise HTTPException(status_code=500, detail=str(e))
