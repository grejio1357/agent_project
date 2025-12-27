import faiss
import numpy as np
from typing import List
from langchain_huggingface import HuggingFaceEmbeddings


class FaissService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="jhgan/ko-sroberta-multitask"
        )

    def search(
        self,
        query: str,
        candidates: List[str],
        top_k: int = 5
    ) -> List[str]:
        """
        FAISS search on candidate documents only
        """

        if not candidates:
            return []

        # 후보 문서 임베딩
        doc_vectors = self.embeddings.embed_documents(candidates)
        doc_vectors = np.array(doc_vectors, dtype="float32")

        dim = doc_vectors.shape[1]

        # 임시 FAISS index 생성 (in-memory)
        index = faiss.IndexFlatL2(dim)
        index.add(doc_vectors)

        # 쿼리 임베딩
        query_vector = self.embeddings.embed_query(query)
        query_vector = np.array([query_vector], dtype="float32")

        # 검색
        distances, indices = index.search(query_vector, top_k)

        # 결과 매핑
        results = []
        for idx in indices[0]:
            if idx != -1:
                results.append(candidates[idx])

        return results
