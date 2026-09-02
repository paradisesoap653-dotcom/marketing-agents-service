import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
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
    image_url: str
    prompt: str
    duration: str = "5"
    aspect_ratio: str = "9:16"


def generate_campaign_text(product_name: str, target_audience: str) -> str:
    """دالة مشتركة بتولد نص الحملة التسويقية وترجعه نظيف بدون رموز Markdown"""
    if not gemini_api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY غير موجود في متغيرات البيئة.")

    client = genai.Client(api_key=gemini_api_key)

    prompt = f"""
    أنت خبير تسويق رقمي محترف.
    قم بكتابة منشور تسويقي مبتكر وجذاب لمنتج: {product_name}
    الجمهور المستهدف: {target_audience}
    شامل الهاشتاجات المناسبة.

    قواعد صارمة للتنسيق (مهم جداً):
    - اكتب نص عادي (plain text) فقط، بدون أي رموز Markdown إطلاقاً.
    - ممنوع استخدام النجمتين ** أو النجمة الواحدة * للتشديد.
    - ممنوع استخدام علامات # للعناوين.
    - استخدم أسطر فارغة حقيقية للفصل بين الفقرات، مش الرمز \\n مكتوب كنص.
    - النتيجة يجب أن تكون جاهزة للنسخ واللصق مباشرة على فيسبوك أو إنستجرام من غير أي تعديل.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        clean_text = response.text
        clean_text = clean_text.replace("\\n", "\n")
        clean_text = clean_text.replace("**", "").replace("*", "")
        clean_text = clean_text.replace("### ", "").replace("## ", "").replace("# ", "")
        clean_text = clean_text.strip()

        return clean_text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google API Error: {str(e)}")


@app.get("/")
def home():
    return {"status": "Service is running perfectly!"}


@app.post("/run-campaign")
def run_campaign(request: CampaignRequest):
    clean_text = generate_campaign_text(request.product_name, request.target_audience)
    return {
        "success": True,
        "model_used": "gemini-3.6-flash",
        "result": clean_text
    }


@app.get("/run-campaign-text", response_class=PlainTextResponse)
def run_campaign_text(product_name: str, target_audience: str):
    """
    نفس /run-campaign بالظبط، لكن بيرجع النص كـ plain text خام
    بدون أي JSON أو رموز \\n ظاهرة — جاهز للنسخ واللصق المباشر.
    """
    return generate_campaign_text(product_name, target_audience)


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
