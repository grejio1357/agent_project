from pydantic import BaseModel
from typing import Optional, List, Any


class QueryResponse(BaseModel):
    """
    Response schema to frontend.
    """
    answer: str
    sql_result: Optional[List[Any]] = None
    rag_docs: Optional[List[str]] = None
