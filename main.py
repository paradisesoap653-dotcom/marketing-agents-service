import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process, LLM

# ضبط مفتاح Gemini بكافة الأشكال التي قد تطلبها LiteLLM
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    os.environ["GEMINI_API_KEY"] = api_key
    os.environ["GOOGLE_API_KEY"] = api_key

app = FastAPI(title="Marketing Agents Service")

executor = ThreadPoolExecutor(max_workers=3)

class CampaignRequest(BaseModel):
    product_name: str
    target_audience: str

@app.get("/")
def home():
    return {"status": "Marketing Agents Service is running online!"}

def execute_crew(product_name: str, target_audience: str):
    # استخدام اسم الموديل المباشر
    gemini_llm = LLM(
        model="gemini-1.5-flash", 
        api_key=api_key
    )

    marketer = Agent(
        role='خبير تسويق رقمي',
        goal=f'إنشاء خطة تسويقية جذابة لمنتج {product_name}',
        backstory='أنت خبير محترف في كتابة الحملات الإعلانية وجذب الجمهور المستهدف.',
        verbose=True,
        llm=gemini_llm
    )

    task = Task(
        description=f'قم بكتابة منشور تسويقي مبتكر لمنتج {product_name} موجه لـ {target_audience}.',
        expected_output='منشور إعلاني مكتمل وجاهز للنشر مع الهاشتاجات المناسبة.',
        agent=marketer
    )

    crew = Crew(
        agents=[marketer],
        tasks=[task],
        process=Process.sequential
    )

    result = crew.kickoff()
    return str(result)

@app.post("/run-campaign")
async def run_campaign(request: CampaignRequest):
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor, 
            execute_crew, 
            request.product_name, 
            request.target_audience
        )
        return {"success": True, "result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
