import re


def classify_question(question: str) -> str:
    """
    Classify user question into one of:
    - 'sql'      : numeric / aggregation questions
    - 'rag'      : conceptual / explanatory questions
    - 'sql_rag'  : numeric + explanation
    """

    q = question.lower()

    # =========================
    # SQL-only signals
    # =========================
    sql_keywords = [
        "얼마", "몇", "총", "합계", "평균", "최대", "최소",
        "수치", "통계", "비율", "증가", "감소",
        "sum", "avg", "count", "max", "min"
    ]

    # =========================
    # RAG-only signals
    # =========================
    rag_keywords = [
        "왜", "이유", "차이", "특징", "장점", "단점",
        "어떤", "어떻게", "비교", "설명",
        "재배", "환경", "조건", "관리"
    ]

    sql_hit = any(k in q for k in sql_keywords)
    rag_hit = any(k in q for k in rag_keywords)

    # =========================
    # Routing logic
    # =========================
    if sql_hit and rag_hit:
        return "sql_rag"

    if sql_hit:
        return "sql"

    return "rag"
