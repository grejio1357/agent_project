import pickle
import faiss
from langchain_openai import OpenAIEmbeddings
from app.core.settings import settings


class FaissService:
    def __init__(self):
        self.index = faiss.read_index("db/faiss/faiss.index")

        with open("db/faiss/metadata.pkl", "rb") as f:
            self.documents = pickle.load(f)

        self.embeddings = OpenAIEmbeddings(
            api_key=settings.openai_api_key
        )

    def search(self, query: str, top_k: int = 5) -> list[str]:
        """
        Return top_k relevant document texts.
        """
        query_vector = self.embeddings.embed_query(query)
        distances, indices = self.index.search(
            [query_vector], top_k
        )

        results = []
        for idx in indices[0]:
            if idx != -1:
                results.append(self.documents[idx].page_content)

        return results
