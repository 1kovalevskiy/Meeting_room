from app.crud.base import CRUDBase
from app.models.reservation import Reservation

reservation_crud = CRUDBase(Reservation)