from app.agents.sql_agent import SQLAgent
from app.agents.validator_agent import ValidatorAgent
from app.agents.normalizer_agent import NormalizerAgent

sql_agent = SQLAgent()
normalizer = NormalizerAgent()
validator = ValidatorAgent()

def run_workflow(state):
    # 1. SQL 생성
    sql = sql_agent.run(state)
    state.generated_sql = sql

    # 2. SQL 정규화 (지역명 등)
    normalized_sql = normalizer.normalize(sql)
    state.normalized_sql = normalized_sql

    # 3. SQL 검증
    validation = validator.validate(normalized_sql)

    if not validation.is_valid:
        state.retry_count += 1
        state.last_error = validation.reason
        return state  # retry loop로 돌아감

    # 4. DB 실행 (다음 단계)
    return state
