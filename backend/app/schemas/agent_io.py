from pydantic import BaseModel
from typing import Optional

class ValidationResult(BaseModel):
    is_valid: bool
    reason: Optional[str] = None