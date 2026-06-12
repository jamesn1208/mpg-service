from pydantic import BaseModel
from typing import Literal


class HealthReport(BaseModel):
    status: Literal["ok", "warning", "error"] = "ok"
    message: str
