from datetime import date

from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):

    model = RoomsORM
    schema = Room

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to, hotel_id=hotel_id)
        return await self.get_filtered(RoomsORM.id.in_(rooms_ids_to_get))
