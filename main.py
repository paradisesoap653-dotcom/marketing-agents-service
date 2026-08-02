import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process

app = FastAPI(title="Marketing Agents Service")

# نموذج لاستقبال البيانات
class CampaignRequest(BaseModel):
    product_name: str
    target_audience: str

@app.get("/")
def home():
    return {"status": "Marketing Agents Service is running online!"}

@app.post("/run-campaign")
def run_campaign(request: CampaignRequest):
    try:
        # 1. تعريف وكيل التسويق
        marketer = Agent(
            role='خبير تسويق رقمي',
            goal=f'إنشاء خطة تسويقية جذابة لمنتج {request.product_name}',
            backstory='أنت خبير محترف في كتابة الحملات الإعلانية وجذب الجمهور المستهدف.',
            verbose=True
        )

        # 2. تحديد المهمة
        task = Task(
            description=f'قم بكتابة منشور تسويقي مبتكر لمنتج {request.product_name} موجه لـ {request.target_audience}.',
            expected_output='منشور إعلاني مكتمل وجاهز للنشر مع الهاشتاجات المناسبة.',
            agent=marketer
        )

        # 3. تشغيل الفريق
        crew = Crew(
            agents=[marketer],
            tasks=[task],
            process=Process.sequential
        )

        result = crew.kickoff()
        return {"success": True, "result": str(result)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
