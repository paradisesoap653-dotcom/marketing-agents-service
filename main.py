import os
from fastapi import FastAPI
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process

app = FastAPI()

# تهيئة اسم النموذج كـ string متوافق مع CrewAI
GEMINI_MODEL = "gemini/gemini-1.5-flash"

# 1. Agent لخدمة Paradise Soap
paradise_agent = Agent(
    role="مستشار ومُستقطب البائعين لمنصة Paradise Soap",
    goal="مساعدة منتجي الصابون والعناية الطبيعية للمنصة كبائعين، ومساعدة المشتريين",
    backstory="أنت خبير المبيعات لمنصة Paradise Soap. تشجع البائعين الجدد بالضغط على 'انضم كبائع' والتسجيل لعرض منتجاتهم بأسلوب جذاب وداعم.",
    verbose=True,
    allow_delegation=False,
    llm=GEMINI_MODEL
)

# 2. Agent لتطبيق Rakshatak
rakshatak_agent = Agent(
    role="مساعد دعم عملاء وسائقين لتطبيق ركشتك (Rakshatak)",
    goal="مساعدة السائقين للتسجيل في التطبيق لحجز رحلات نقل البضائع والركاب",
    backstory="أنت ممثل خدمة العملاء لتطبيق ركشتك. توضح طريقة الانضمام والتسجيل للسائقين وكيفية استقبال طلبات الركاب ونقل البضائع بسهولة.",
    verbose=True,
    allow_delegation=False,
    llm=GEMINI_MODEL
)

@app.get("/")
def home():
    return {"status": "Marketing Agents Service is running online!"}
