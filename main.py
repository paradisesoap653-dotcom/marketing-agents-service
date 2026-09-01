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

    client = genai.Client(api_key=gemini_api_key)

    prompt = f"""
    أنت خبير تسويق رقمي محترف. 
    قم بكتابة منشور تسويقي مبتكر وجذاب لمنتج: {request.product_name}
    الجمهور المستهدف: {request.target_audience}
    شامل الهاشتاجات المناسبة.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return {
            "success": True,
            "model_used": "gemini-2.5-flash",
            "result": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google API Error: {str(e)}")


@app.post("/generate-video-ad")
def generate_video_ad(request: VideoAdRequest):
    if not fal_api_key:
        raise HTTPException(status_code=500, detail="FAL_KEY غير موجود في متغيرات البيئة.")

    os.environ["FAL_KEY"] = fal_api_key

    try:
        result = fal_client.subscribe(
            "fal-ai/kling-video/v2.1/standard/image-to-video",
            arguments={
                "prompt": request.prompt,
                "image_url": request.image_url,
                "duration": request.duration,
                "aspect_ratio": request.aspect_ratio,
            },
        )
        return {
            "success": True,
            "model_used": "kling-video-v2.1-standard",
            "video_url": result["video"]["url"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"fal.ai API Error: {str(e)}")
