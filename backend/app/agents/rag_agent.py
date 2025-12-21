from app.services.faiss_service import FaissService
from app.core.llm import llm
from app.prompts.rag_prompt import SYSTEM_PROMPT, RAG_TEMPLATE

class RAGAgent:
    def __init__(self):
        self.faiss = FaissService()

    def run(self, question: str) -> str:
        docs = self.faiss.search(question)

        if not docs:
            return "죄송합니다. 관련 정보를 찾을 수 없습니다."

        context = "\n\n".join(docs)
        formatted_prompt = RAG_TEMPLATE.format(context=context, question=question)
        prompt = f"{SYSTEM_PROMPT}\n\n{formatted_prompt}"

        try:
            response = llm.invoke(prompt)
            return response.content.strip()
        except Exception as e:
            return f"LLM 호출 중 오류가 발생했습니다: {e}"
