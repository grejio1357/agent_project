from typing import List
from app.services.faiss_service import FaissService
from app.services.opensearch_service import OpenSearchService
from app.core.llm import LLMService
from app.prompts.rag_prompt import SYSTEM_PROMPT, RERANK_INSTRUCTION


class RAGAgent:
    def __init__(self):
        self.faiss = FaissService()
        self.opensearch = OpenSearchService()
        self.llm = LLMService()

    def run(
        self,
        question: str,
        keyword_k: int = 20,
        recall_k: int = 12,
        rerank_n: int = 3
    ) -> List[str]:
        """
        RAG pipeline:
        1. OpenSearch keyword recall
        2. FAISS vector recall (filtered)
        3. LLM-based reranking
        """

        # OpenSearch: 키워드 기반 1차 필터
        keyword_docs = self.opensearch.search(question, top_k=keyword_k)
        if not keyword_docs:
            return []

        # FAISS: 벡터 검색 (keyword_docs 기반)
        vector_docs = self.faiss.search(
            query=question,
            top_k=recall_k,
            candidates=keyword_docs   
        )

        if not vector_docs:
            return []

        # Rerank
        reranked_docs = self._rerank(question, vector_docs, top_n=rerank_n)
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
        indices = []
        for token in response.replace(" ", "").split(","):
            if token.isdigit():
                idx = int(token)
                if 0 <= idx < max_len:
                    indices.append(idx)
        return indices
