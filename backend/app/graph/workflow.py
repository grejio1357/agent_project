from langgraph.graph import StateGraph
from app.schemas.graph_state import GraphState

from app.agents.schema_agent import SchemaAgent
from app.agents.sql_agent import SQLAgent
from app.agents.normalizer_agent import NormalizerAgent
from app.agents.validator_agent import ValidatorAgent
from app.agents.rag_agent import RAGAgent

from app.services.postgres_service import PostgresService
from app.utils.question_classifier import classify_question


# ===== Agent / Service instances =====
schema_agent = SchemaAgent()
sql_agent = SQLAgent()
normalizer = NormalizerAgent()
validator = ValidatorAgent()
rag_agent = RAGAgent()
postgres = PostgresService()


# ===== Node definitions =====

def classify_intent(state: GraphState) -> GraphState:
    state.intent = classify_question(state.question)
    return state


def load_schema(state: GraphState) -> GraphState:
    state.db_schema = schema_agent.run()
    return state


def generate_sql(state: GraphState) -> GraphState:
    state.generated_sql = sql_agent.run(
        question=state.question,
        schema=state.db_schema
    )
    return state


def normalize_and_validate(state: GraphState) -> GraphState:
    state.normalized_sql = normalizer.normalize(state.generated_sql)

    result = validator.validate(state.normalized_sql)
    if not result.is_valid:
        state.retry_count += 1
        state.last_error = result.reason
    else:
        state.last_error = None

    return state


def execute_sql(state: GraphState) -> GraphState:
    state.sql_result = postgres.run(state.normalized_sql)
    return state


def run_rag(state: GraphState) -> GraphState:
    state.rag_docs = rag_agent.run(state.question)
    return state


# ===== Conditional edge helpers =====

def route_by_intent(state: GraphState) -> str:
    if state.intent == "rag":
        return "rag"
    return "sql"   # sql or sql_rag


def check_retry(state: GraphState) -> str:
    if state.last_error and state.retry_count < state.max_retries:
        return "retry"
    return "ok"


def need_rag_after_sql(state: GraphState) -> str:
    if state.intent == "sql_rag":
        return "rag"
    return "end"


# ===== Graph assembly =====

graph = StateGraph(GraphState)

# nodes
graph.add_node("intent", classify_intent)
graph.add_node("schema", load_schema)
graph.add_node("sql", generate_sql)
graph.add_node("validate", normalize_and_validate)
graph.add_node("execute", execute_sql)
graph.add_node("rag", run_rag)

# entry point
graph.set_entry_point("intent")

# intent routing
graph.add_conditional_edges(
    "intent",
    route_by_intent,
    {
        "rag": "rag",
        "sql": "schema",
    }
)

# SQL flow
graph.add_edge("schema", "sql")
graph.add_edge("sql", "validate")

graph.add_conditional_edges(
    "validate",
    check_retry,
    {
        "retry": "sql",
        "ok": "execute",
    }
)

# after SQL
graph.add_conditional_edges(
    "execute",
    need_rag_after_sql,
    {
        "rag": "rag",
        "end": "__end__",
    }
)

# rag-only path end
graph.add_edge("rag", "__end__")

compiled_graph = graph.compile()

