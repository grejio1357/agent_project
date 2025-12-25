from fastapi import FastAPI
from app.api.query import router as query_router

app = FastAPI(
    title="Agricultural AI Agent API")

# API 라우터 등록
app.include_router(
    query_router,
    prefix="/api",
    tags=["query"]
)