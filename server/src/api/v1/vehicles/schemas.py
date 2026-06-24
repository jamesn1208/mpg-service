from pydantic import BaseModel


class VehicleUpdate(BaseModel):
    make: str | None = None
    emissions: float | int | None = None
    year: int | None = None
    colour: str | None = None


class VehicleBase(BaseModel):
    make: str
    emissions: float | int
    year: int
    colour: str


class Vehicle(VehicleBase):
    registration: str
