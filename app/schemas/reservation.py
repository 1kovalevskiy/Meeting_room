from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Field, root_validator, validator


class ReservationBase(BaseModel):
    from_reserve: datetime
    to_reserve: datetime


class ReservationUpdate(ReservationBase):
    pass

    @validator('from_reserve')
    def check_from_reserve_later_than_now(cls, value):
        if datetime.now() > value:
            raise ValueError("Необходимо указать время в будущем")


    @root_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, values):
        if values['from_reserve'] >= values['to_reserve']:
            raise ValueError("Конец не может быть раньше начала")


class ReservationCreate(ReservationUpdate):
    meetingroom_id: int


class ReservationDB(ReservationBase):
    id: int

    class Config:
        orm_mode = True
