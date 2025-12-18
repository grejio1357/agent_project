from app.schemas.agent_io import ValidationResult

class ValidatorAgent:

    BLOCKED_KEYWORDS = [
        "delete", "update", "insert", "drop",
        "truncate", "alter",
        "pg_catalog", "information_schema"
    ]

    def validate(self, sql: str) -> ValidationResult:
        lowered = sql.lower()

        for keyword in self.BLOCKED_KEYWORDS:
            if keyword in lowered:
                return ValidationResult(
                    is_valid=False,
                    reason=f"Blocked SQL keyword detected: {keyword}"
                )

        return ValidationResult(is_valid=True)
