import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

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
        # البحث عن نموذج يعمل تلقائياً لتفادي أخطاء الـ 404
        available_models = [
            m.name for m in genai.list_models() 
            if 'generateContent' in m.supported_generation_methods
        ]
        
        if not available_models:
            raise Exception("لم يتم العثور على أي نموذج داعم للإنشاء بنفس المفتاح.")
            
        # اختيار أول نموذج متاح (مثل models/gemini-1.5-flash أو الأحدث)
        selected_model_name = available_models[0]
        model = genai.GenerativeModel(selected_model_name)
        
        prompt = f"""
        أنت خبير تسويق رقمي محترف. 
        قم بكتابة منشور تسويقي مبتكر وجذاب لمنتج: {request.product_name}
        الجمهور المستهدف: {request.target_audience}
        شامل الهاشتاجات المناسبة.
        """
        
        response = model.generate_content(prompt)
        
        return {
            "success": True, 
            "used_model": selected_model_name,
            "result": response.text
        }

    except Exception as e:
        print(f"Error details: {e}")
        raise HTTPException(status_code=500, detail=str(e))
