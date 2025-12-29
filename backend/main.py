from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.query import router as query_router

app = FastAPI(
    title="Agricultural AI Agent API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React server
    ],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(
    query_router,
    prefix="/api",
    tags=["query"]
)
