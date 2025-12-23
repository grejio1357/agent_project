from fastapi import APIRouter, HTTPException

from app.schemas.query import QueryRequest
from app.schemas.response import QueryResponse
from app.schemas.graph_state import GraphState

from app.graph.workflow import compiled_graph
from app.agents.synthesizer_agent import SynthesizerAgent


router = APIRouter()
synthesizer = SynthesizerAgent()


@router.post("/query", response_model=QueryResponse)
def query_api(req: QueryRequest):
    """
    Entry point for user questions.
    1. Create initial GraphState
    2. Run LangGraph workflow
    3. Synthesize final answer
    4. Return response to frontend
    """

    try:
        # 1️⃣ 초기 State 생성 (사용자 질문)
        state = GraphState(
            question=req.question
        )

        # 2️⃣ LangGraph 실행 → state 채워짐
        final_state: GraphState = compiled_graph.invoke(state)

        # 3️⃣ SynthesizerAgent로 최종 답변 생성
        answer = synthesizer.run(
            question=final_state.question,
            sql_result=final_state.sql_result,
            rag_docs=final_state.rag_docs,
        )

        # 4️⃣ Frontend로 응답 반환
        return QueryResponse(
            answer=answer,
            sql_result=final_state.sql_result,
            rag_docs=final_state.rag_docs,
        )

    except Exception as e:
        # 예상 못 한 오류에 대한 안전망
        raise HTTPException(
            status_code=500,
            detail=f"Query processing failed: {str(e)}"
        )
