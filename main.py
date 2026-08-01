import os
from fastapi import FastAPI
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

app = FastAPI()

# تهيئة نموذج Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.environ.get("GEMINI_API_KEY")
)

# 1. Agent لخدمة Paradise Soap (البائعين والمشترين)
paradise_agent = Agent(
    role="مستشار ومُستقطب البائعين لمنصة Paradise Soap",
    goal="شرح كيفية انضمام منتجي الصابون والعناية الطبيعية للمنصة كبائعين، ومساعدة المشترين.",
    backstory="""أنت خبير المبيعات لمنصة Paradise Soap. 
    تشجع المنتجين على الضغط على 'انضم كبائع' والتسجيل لعرض منتجاتهم بأسلوب جذاب وداعم.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# 2. Agent لتطبيق Rakshatak (السائقين والركاب)
rakshatak_agent = Agent(
    role="مساعد دعم عملاء وسائقين لتطبيق ركشتك (Rakshatak)",
    goal="مساعدة السائقين للتسجيل وتوجيه الركاب لطلب رحلات ونقل البضائع.",
    backstory="""أنت المساعد المباشر لتطبيق ركشتك المتخصص في الترحال والنقل بالركشات والشحن.
    تجيب بأسلوب مبسط لإرشادهم لتنزيل التطبيق واستخدامه.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

class AgentRequest(BaseModel):
    platform: str  # "paradise" or "rakshatak"
    message: str

@app.get("/")
def home():
    return {"status": "Marketing Agents Service is Running!"}

@app.post("/chat")
def chat_with_agent(req: AgentRequest):
    selected_agent = paradise_agent if req.platform == "paradise" else rakshatak_agent
    
    task = Task(
        description=f"قم بالرد على الرسالة التالية: '{req.message}'",
        expected_output="رد وافي ومباشر باللغة العربية يناسب الخدمة المطلوبة.",
        agent=selected_agent
    )
    
    crew = Crew(
        agents=[selected_agent],
        tasks=[task],
        process=Process.sequential
    )
    
    result = crew.kickoff()
    return {"response": str(result)}
