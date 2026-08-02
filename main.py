import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai

# جلب المفتاح من متغيرات البيئة
api_key = os.getenv("GEMINI_API_KEY")

app = FastAPI(title="Marketing Service")

class CampaignRequest(BaseModel):
    product_name: str
    target_audience: str

@app.get("/")
def home():
    return {"status": "Service is running perfectly!"}

@app.post("/run-campaign")
def run_campaign(request: CampaignRequest):
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY غير موجود في متغيرات البيئة.")

    try:
        # إنشاء العميل باستخدام المكتبة الجديدة google-genai
        client = genai.Client(api_key=api_key)

        prompt = f"""
        أنت خبير تسويق رقمي محترف. 
        قم بكتابة منشور تسويقي مبتكر وجذاب لمنتج: {request.product_name}
        الجمهور المستهدف: {request.target_audience}
        شامل الهاشتاجات المناسبة.
        """

        # الاستدعاء الصحيح وفقاً للمكتبة الحديثة
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
        )

        return {
            "success": True, 
            "model_used": "gemini-2.0-flash",
            "result": response.text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API Error: {str(e)}")
