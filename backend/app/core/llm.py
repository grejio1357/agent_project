from langchain_openai import ChatOpenAI
from app.core.settings import settings

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=settings.openai_api_key
)
