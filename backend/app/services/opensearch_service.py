from opensearchpy import OpenSearch, helpers
from app.core.settings import settings
from typing import List, Dict
import json

class OpenSearchService:
    def __init__(self):
        """
        OpenSearch 클라이언트 초기화
        """
        self.client = OpenSearch(
            hosts=[{
                "host": settings.OPENSEARCH_HOST,
                "port": settings.OPENSEARCH_PORT
            }],
            use_ssl=settings.OPENSEARCH_USE_SSL,
            verify_certs=False
        )

        self.index_name = settings.OPENSEARCH_INDEX

    def create_index_if_not_exists(self):
        """
        RAG용 OpenSearch index 생성
        (이미 존재하면 생성하지 않음)
        """
        if self.client.indices.exists(index=self.index_name):
            return

        index_body = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "korean_analyzer": {
                            "type": "standard"
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "content": {
                        "type": "text",
                        "analyzer": "korean_analyzer"
                    },
                    "crop": {
                        "type": "keyword"
                    },
                    "section": {
                        "type": "keyword"
                    },
                    "page_range": {
                        "type": "keyword"
                    }
                }
            }
        }

        self.client.indices.create(
            index=self.index_name,
            body=index_body
        )

    def load_jsonl(self, path: str) -> List[Dict]:
        """
        jsonl 파일 로드
        """
        documents = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                documents.append(json.loads(line))
        return documents

    def bulk_ingest(self, documents: List[Dict]):
        """
        문서 bulk 저장
        """
        actions = []

        for i, doc in enumerate(documents):
            actions.append({
                "_index": self.index_name,
                "_id": i,
                "_source": doc
            })

        helpers.bulk(self.client, actions)

    def search(self, query: str, top_k: int = 10) -> List[str]:
        """
        키워드 기반 검색
        """
        body = {
            "size": top_k,
            "query": {
                "match": {
                    "content": query
                }
            }
        }

        res = self.client.search(
            index=self.index_name,
            body=body
        )

        hits = res["hits"]["hits"]
        return [hit["_source"]["content"] for hit in hits]
