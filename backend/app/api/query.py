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
        state = GraphState(
            question=req.question
        )

        final_state: GraphState = compiled_graph.invoke(state)

        answer = synthesizer.run(
            question=final_state['question'],
            sql_result=final_state.get('sql_result', []),
            rag_docs=final_state.get('rag_docs', []),
        )

        return QueryResponse(
            answer=answer,
            sql_result=final_state.get("sql_result", []),
            rag_docs=final_state.get('rag_docs', []),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Query processing failed: {str(e)}"
        )
