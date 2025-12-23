from pydantic import BaseModel


class QueryRequest(BaseModel):
    """
    Request schema from frontend.
    """
    question: str
