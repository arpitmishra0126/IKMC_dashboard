from typing import Any

from pydantic import BaseModel


class ValidationDetailResponse(BaseModel):
    check: str
    row_count: int
    columns: list[str]
    records: list[dict[str, Any]]
