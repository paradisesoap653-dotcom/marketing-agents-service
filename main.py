import os
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai.errors import APIError

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

    prompt = f"""
    أنت خبير تسويق رقمي محترف. 
    قم بكتابة منشور تسويقي مبتكر وجذاب لمنتج: {request.product_name}
    الجمهور المستهدف: {request.target_audience}
    شامل الهاشتاجات المناسبة.
    """

    # قائمة الموديلات مرتبة حسب الأولوية للتراجع عند وجود Quota limit
    candidate_models = [
        'gemini-1.5-flash',
        'gemini-2.0-flash',
        'gemini-1.5-pro'
    ]

    last_error = None

    for model_name in candidate_models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            return {
                "success": True,
                "used_model": model_name,
                "result": response.text
            }
        except APIError as e:
            last_error = e
            # إذا كان الخطأ 429 (Quota Exhausted) نجرب الموديل التالي مباشرة
            if e.code == 429:
                continue
            else:
                raise HTTPException(status_code=500, detail=f"API Error ({model_name}): {str(e)}")
        except Exception as e:
            last_error = e
            continue

    # في حال فشل جميع الموديلات بسبب Quota Limit
    raise HTTPException(
        status_code=429, 
        detail=f"تجاوز حدود الاستخدام لجميع النماذج المجانية. يرجى محاولة إنشاء مفتاح API جديد من Google AI Studio أو الانتظار قليلاً. التفاصيل: {str(last_error)}"
    )
