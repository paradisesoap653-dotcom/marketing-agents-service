import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
import fal_client

gemini_api_key = os.getenv("GEMINI_API_KEY")
fal_api_key = os.getenv("FAL_KEY")

app = FastAPI(title="Marketing Service")


class CampaignRequest(BaseModel):
    product_name: str
    target_audience: str


class VideoAdRequest(BaseModel):
    image_url: str          # رابط صورة المنتج (لازم يكون رابط عام متاح على الإنترنت)
    prompt: str              # وصف الحركة/المشهد المطلوب للفيديو
    duration: str = "5"      # المدة بالثواني (5 أو 10 حسب الموديل)
    aspect_ratio: str = "9:16"  # 9:16 للـ Reels/Stories أو 16:9 لليوتيوب


@app.get("/")
def home():
    return {"status": "Service is running perfectly!"}


@app.post("/run-campaign")
def run_campaign(request: CampaignRequest):
    if not gemini_api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY غير موجود في متغيرات البيئة.")

    client =
