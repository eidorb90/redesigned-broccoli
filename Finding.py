from pydantic import BaseModel


class Finding(BaseModel):
    rule_id: str
    file: str
    line: int
    message: str
    confidence: float = 0.9
