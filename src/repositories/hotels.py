from datetime import date

from sqlalchemy import select

from src.exceptions import WrongDateOrderException
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.utils import rooms_ids_for_booking


class HotelsRepository(BaseRepository):
    model = HotelsORM
    mapper = HotelDataMapper

    async def get_filtered_by_time(
        self,
        limit: int,
        offset: int,
        date_from: date,
        date_to: date,
        title: str,
        location: str,
    ):
        if date_from > date_to:
            raise WrongDateOrderException
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )

        query = select(HotelsORM).filter(HotelsORM.id.in_(hotels_ids_to_get))
        if title:
            query = query.filter(HotelsORM.title.ilike(f"%{title}%"))
        if location:
            query = query.filter(HotelsORM.location.ilike(f"%{location}%"))

        query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]
