from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Field, root_validator, validator, Extra, UUID4

FROM_TIME = (
    datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')

TO_TIME = (
    datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')


class ReservationBase(BaseModel):
    from_reserve: datetime = Field(..., example=FROM_TIME)
    to_reserve: datetime = Field(..., example=TO_TIME)

    class Config:
        extra = Extra.forbid


class ReservationUpdate(ReservationBase):
    pass

    @validator('from_reserve')
    def check_from_reserve_later_than_now(cls, value):
        if datetime.now() > value:
            raise ValueError("Необходимо указать время в будущем")
        return value

    @root_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, values):
        if values['from_reserve'] >= values['to_reserve']:
            raise ValueError("Конец не может быть раньше начала")
        return values


class ReservationCreate(ReservationUpdate):
    meetingroom_id: int


class ReservationDB(ReservationBase):
    id: int
    user_id: Optional[UUID4]

    class Config:
        orm_mode = True
