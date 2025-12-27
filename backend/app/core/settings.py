from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # OpenAI
    openai_api_key: str
    
    # FAISS
    FAISS_INDEX_PATH: str = "db/faiss/faiss.index"
    FAISS_METADATA_PATH: str = "db/faiss/metadata.pkl"

    # OpenSearch 
    OPENSEARCH_HOST: str = "localhost"
    OPENSEARCH_PORT: int = 9200
    OPENSEARCH_INDEX: str = "rag_documents"
    OPENSEARCH_USE_SSL: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
