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
    try:
        state = GraphState(
            question=req.question
        )

        final_state: GraphState = compiled_graph.invoke(state)

        answer = synthesizer.run(
            question=final_state['question'],              
            sql_result=final_state['sql_result'] or [],    
            rag_docs=final_state['rag_docs'] or [],        
        )

        return QueryResponse(
            answer=answer,
            sql_result=final_state['sql_result'] or [],
            rag_docs=final_state['rag_docs'] or [],
        )

    except Exception as e:
        import traceback
        traceback.print_exc()   #(디버그용)
        raise HTTPException(
            status_code=500,
            detail=f"Query processing failed: {str(e)}"
        )

