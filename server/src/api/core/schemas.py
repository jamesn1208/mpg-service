from pydantic import BaseModel
from fastapi import Query
from typing import Annotated


type LIMIT = Annotated[int, Query(title="The amount of records to return", ge=1, le=250)]
type OFFSET = Annotated[int, Query(title="The 0 indexed page number", ge=0)]


class NotYetImplemented(BaseModel):
    detail: str


class ActionResponse(BaseModel):
    message: str
    success: bool
