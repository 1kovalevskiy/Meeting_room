from datetime import datetime
from typing import Optional, List, Dict

from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import and_, between, or_, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.reservation import Reservation
from app.schemas.user import UserDB


class CRUDReservation(CRUDBase):

    async def get_reservations_at_the_same_time(
            self,
            *,
            from_reserve: datetime,
            to_reserve: datetime,
            meetingroom_id: int,
            reservation_id: Optional[int] = None,
            session: AsyncSession,
    ) -> List[Reservation]:

        select_stmt = select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id
        ).where(
            or_(
                between(Reservation.to_reserve, from_reserve, to_reserve),
                between(Reservation.from_reserve, from_reserve, to_reserve),
                and_(
                    Reservation.from_reserve >= from_reserve,
                    Reservation.to_reserve <= to_reserve
                )
            )
        )
        if reservation_id is not None:
            select_stmt = select_stmt.where(
                Reservation.id != reservation_id
            )
        reservations = await session.execute(select_stmt)
        reservations = reservations.scalars().all()
        return reservations

    async def get_future_reservations_for_room(
            self,
            room_id: int,
            session: AsyncSession,
    ):
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.meetingroom_id == room_id,
                Reservation.to_reserve > datetime.now()
            )
        )
        reservations = reservations.scalars().all()
        return reservations

    async def get_by_user(
            self,
            session: AsyncSession,
            user: UserDB,
    ):
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.user_id == user.id,
                Reservation.to_reserve > datetime.now()
            )
        )
        reservations = reservations.scalars().all()
        return reservations

    async def get_count_res_at_the_same_time(
            self,
            from_reserve: datetime,
            to_reserve: datetime,
            session: AsyncSession,
    ) -> List[Dict[str, int]]:
        reservations = await session.execute(
            select([Reservation.meetingroom_id,
                    func.count(Reservation.meetingroom_id)]).where(
                Reservation.from_reserve >= from_reserve,
                Reservation.to_reserve <= to_reserve
            ).group_by(Reservation.meetingroom_id)
        )
        reservations = reservations.all()
        return reservations


reservation_crud = CRUDReservation(Reservation)
