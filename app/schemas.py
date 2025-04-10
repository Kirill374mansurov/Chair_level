from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional


class TableBase(BaseModel):
    name: str
    seats: int
    location: str


class TableCreate(TableBase):
    pass


class Table(TableBase):
    id: int

    class Config:
        orm_mode = True


class ReservationBase(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int

    @validator('duration_minutes')
    def duration_positive(cls, v):
        if v <= 0:
            raise ValueError('Duration must be positive')
        return v


class ReservationCreate(ReservationBase):
    pass


class Reservation(ReservationBase):
    id: int

    class Config:
        orm_mode = True
