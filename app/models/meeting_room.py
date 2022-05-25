from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models.reservation import Reservation


class MeetingRoom(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    reservations = relationship(Reservation, cascade='delete')
