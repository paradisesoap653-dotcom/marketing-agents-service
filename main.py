import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

# تهيئة نموذج الذكاء الاصطناعي Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.environ.get("GEMINI_API_KEY")
)

# 1. تعريف Agent لمنصة Paradise Soap (تركيز على البائعين والمشترين)
paradise_agent = Agent(
    role="مستشار ومُستقطب البائعين لمنصة Paradise Soap",
    goal="شرح كيفية انضمام منتجي الصابون والعناية الطبيعية للمنصة كبائعين، ومساعدة المشترين في اختيار المنتجات.",
    backstory="""أنت خبير في المبيعات والتسويق لمنصة Paradise Soap. 
    هدف الرئيسي هو تشجيع المنتجين وأصحاب مشاريع الصابون اليدوي والعناية بالبشرة على الضغط على 'انضم كبائع' والتسجيل بالمنصة لعرض منتجاتهم. 
    تتميز بأسلوب مهني، داعم، ومقنع.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# 2. تعريف Agent لتطبيق Rakshatak
rakshatak_agent = Agent(
    role="مساعد دعم عملاء وسائقين لتطبيق ركشتك (Rakshatak)",
    goal="مساعدة السائقين للتسجيل في التطبيق وتوجيه الركاب لطلب رحلات ونقل البضائع.",
    backstory="""أنت المساعد المباشر لتطبيق ركشتك المتخصص في الترحال والنقل بالشحن والركشات.
    تجيب بأسلوب مبسط وواضح لخدمة السائقين والركاب وإرشادهم لتنزيل التطبيق واستخدامه.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

def run_agent_query(platform, user_message):
    selected_agent = paradise_agent if platform == "paradise" else rakshatak_agent
    
    task = Task(
        description=f"قم بالرد على رسالة العميل التالية بناءً على دورك: '{user_message}'",
        expected_output="رد وافي ومباشر باللغة العربية يناسب الخدمة المطلوبة.",
        agent=selected_agent
    )
    
    crew = Crew(
        agents=[selected_agent],
        tasks=[task],
        process=Process.sequential
    )
    
    return crew.kickoff()

if __name__ == "__main__":
    # تجربة سريعة عند التشغيل
    test_response = run_agent_query("paradise", "كيف يمكنني عرض منتجاتي من الصابون الطبيعي عندكم؟")
    print("\n--- نتيجة التجربة ---")
    print(test_response)
