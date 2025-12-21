from dataclasses import dataclass
from typing import Optional, List, Any

@dataclass
class GraphState:
    question: str
    intent: Optional[str] = None
    db_schema: Optional[dict] = None
    generated_sql: Optional[str] = None
    normalized_sql: Optional[str] = None
    sql_result: Optional[List[Any]] = None
    rag_docs: Optional[List[str]] = None
    retry_count: int = 0
    max_retries: int = 3
    last_error: Optional[str] = None
