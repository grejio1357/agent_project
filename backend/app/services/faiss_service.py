import pickle
import faiss
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.settings import settings
from typing import List
import numpy as np
from app.core.config import RAG_TOP_K


class FaissService:
    def __init__(self):
        try:
            self.index = faiss.read_index(settings.FAISS_INDEX_PATH)
        except Exception as e:
            raise FileNotFoundError(f"FAISS index 파일을 찾을 수 없습니다: {settings.FAISS_INDEX_PATH}") from e

        try:
            with open(settings.FAISS_METADATA_PATH, "rb") as f:
                self.documents = pickle.load(f)
        except Exception as e:
            raise FileNotFoundError(f"FAISS metadata 파일을 찾을 수 없습니다: {settings.FAISS_METADATA_PATH}") from e

        self.embeddings = HuggingFaceEmbeddings(
            model_name="jhgan/ko-sroberta-multitask"
        )

    def search(self, query: str, top_k: int = 5) -> List[str]:
        """
        Search FAISS index.
        If top_k is None, use default from config.
        """
        k = top_k or RAG_TOP_K

        query_vector = self.embeddings.embed_query(query)
        query_vector = np.array(query_vector, dtype='float32')
        
        distances, indices = self.index.search(
            np.array([query_vector]), k
        )

        results = []
        for idx in indices[0]:
            if idx != -1:
                results.append(self.documents[idx].page_content)
        return results


