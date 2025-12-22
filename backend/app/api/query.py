from fastapi import APIRouter
from app.schemas.query import QueryRequest
from app.schemas.response import QueryResponse
from app.schemas.graph_state import GraphState
from app.graph.workflow import compiled_graph
from app.agents.synthesizer_agent import SynthesizerAgent

router = APIRouter()
synthesizer = SynthesizerAgent()


@router.post("/query", response_model=QueryResponse)
def query_api(req: QueryRequest):
    # 1️⃣ GraphState 생성
    state = GraphState(question=req.question)

    # 2️⃣ LangGraph 실행 → state 완성
    final_state = compiled_graph.invoke(state)

    # 3️⃣ SynthesizerAgent 호출
    answer = synthesizer.run(
        question=final_state.question,
        sql_result=final_state.sql_result,
        rag_docs=final_state.rag_docs
    )

    # 4️⃣ Frontend 응답 생성
    return QueryResponse(
        answer=answer,
        sql_result=final_state.sql_result
    )
