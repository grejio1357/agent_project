from typing import List
from app.services.faiss_service import FaissService
from app.core.llm import LLMService
from app.prompts.rag_prompt import SYSTEM_PROMPT, RERANK_INSTRUCTION

class RAGAgent:
    def __init__(self):
        self.faiss = FaissService()
        self.llm = LLMService()

    def run(self, question: str, recall_k: int = 12, rerank_n: int = 3) -> List[str]:
        """
        RAG pipeline:
        1. Vector recall (FAISS)
        2. LLM-based reranking
        """
        # 1️⃣ Recall
        docs = self.faiss.search(question, top_k=recall_k)
        if not docs:
            return []

        # 2️⃣ Rerank
        reranked_docs = self._rerank(question, docs, top_n=rerank_n)
        return reranked_docs

    def _rerank(self, question: str, docs: List[str], top_n: int) -> List[str]:
        """
        LLM-based reranking.
        """
        prompt = self._build_rerank_prompt(question, docs, top_n)
        response = self.llm.invoke(prompt)

        indices = self._parse_indices(response, len(docs))
        selected = indices if indices else list(range(len(docs)))

        return [docs[i] for i in selected[:top_n]]

    def _build_rerank_prompt(self, question: str, docs: List[str], top_n: int) -> str:
        """
        Build LLM prompt for reranking with dynamic top_n.
        """
        doc_block = "\n\n".join([f"[{i}] {doc}" for i, doc in enumerate(docs)])
        return f"""
{SYSTEM_PROMPT}

질문:
{question}

{RERANK_INSTRUCTION.format(top_n=top_n)}

문서:
{doc_block}

출력 형식:
문서 번호만 쉼표로 구분해서 출력 (예: 0,2,5)
"""

    def _parse_indices(self, response: str, max_len: int) -> List[int]:
        """
        Parse LLM output safely.
        """
        indices = []
        for token in response.replace(" ", "").split(","):
            if token.isdigit():
                idx = int(token)
                if 0 <= idx < max_len:
                    indices.append(idx)
        return indices


