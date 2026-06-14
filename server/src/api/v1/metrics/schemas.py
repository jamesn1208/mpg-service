from pydantic import BaseModel
from dataclasses import dataclass
from sqlalchemy import Select
from typing import Any


class Metric(BaseModel):
    title: str
    description: str
    value: str


@dataclass(frozen=True)
class MetricQuery:
    title: str
    description: str
    query: Select[Any]
