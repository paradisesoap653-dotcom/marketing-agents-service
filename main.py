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

    # إضافة البادئة المباشرة models/ المعرفية لـ v1beta
    candidate_models = [
        'models/gemini-1.5-flash',
        'models/gemini-1.5-pro',
        'models/gemini-2.0-flash'
    ]

    errors = []

    for model_name in candidate_models:
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
        except Exception as e:
            errors.append(f"{model_name}: {str(e)}")
            continue

    raise HTTPException(status_code=500, detail=f"Google API Errors: { ' | '.join(errors) }")
