from typing import Optional

from pydantic import BaseModel, Field, validator


class MeetingRoomBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]


class MeetingRoomCreate(MeetingRoomBase):
    name: str = Field(..., min_length=1, max_length=100)


class MeetingRoomUpdate(MeetingRoomBase):
    pass

    @validator('name')
    def check_name_isnt_null(cls, value):
        if not value:
            raise ValueError('Имя не может быть пустым')


class MeetingRoomDB(MeetingRoomCreate):
    id: int

    class Config:
        orm_mode = True
