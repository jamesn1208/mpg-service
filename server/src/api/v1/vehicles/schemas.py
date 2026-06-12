from pydantic import BaseModel


class Vehicle(BaseModel):
    registration: str
    make: str
    emissions: float | int
    year: int
    colour: str
