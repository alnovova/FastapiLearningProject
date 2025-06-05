from datetime import date

from sqlalchemy import select

from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):

    model = HotelsORM
    schema = Hotel

    async def get_filtered_by_time(
            self,
            limit: int,
            offset: int,
            date_from: date,
            date_to: date,
            title: str,
            location: str
    ) -> list[Hotel]:

        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )
        if title:
            hotels_ids_to_get = hotels_ids_to_get.filter(HotelsORM.title.ilike(f"%{title}%"))
        if location:
            hotels_ids_to_get = hotels_ids_to_get.filter(HotelsORM.location.ilike(f"%{location}%"))

        hotels_ids_to_get = hotels_ids_to_get.limit(limit).offset(offset)

        return await self.get_filtered(HotelsORM.id.in_(hotels_ids_to_get))