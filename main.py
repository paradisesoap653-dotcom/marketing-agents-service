import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai

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

    client = genai.Client(api_key=api_key)

    prompt = f"""
    أنت خبير تسويق رقمي محترف. 
    قم بكتابة منشور تسويقي مبتكر وجذاب لمنتج: {request.product_name}
    الجمهور المستهدف: {request.target_audience}
    شامل الهاشتاجات المناسبة.
    """

    # جرب النماذج الأكثر استقراراً في الخطة المجانية
    for model_name in ['gemini-2.5-flash', 'gemini-2.5-flash-lite']:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            return {
                "success": True, 
                "model_used": model_name,
                "result": response.text
            }
        except Exception:
            continue

    raise HTTPException(status_code=429, detail="تم تجاوز الكوتا المجانية مؤقتاً، يرجى المحاولة بعد 15 ثانية.")
