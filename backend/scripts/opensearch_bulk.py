# 딱 한 번만 실행
# 데이터 변경 시에만 재실행
from app.services.opensearch_service import OpenSearchService
from app.core.settings import settings

JSONL_PATH = "db/rag_documents.jsonl"

def main():
    os_service = OpenSearchService()

    print("🔹 Create index if not exists")
    os_service.create_index_if_not_exists()

    print("🔹 Load documents")
    documents = os_service.load_jsonl(JSONL_PATH)
    print(f"Loaded {len(documents)} documents")

    print("🔹 Bulk ingest")
    os_service.bulk_ingest(documents)

    print("✅ OpenSearch bulk ingest completed")

if __name__ == "__main__":
    main()
