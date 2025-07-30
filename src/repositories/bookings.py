from datetime import date

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, and_

from src.models import RoomsORM
from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper, RoomDataMapper
from src.repositories.rooms import RoomsRepository
from src.schemas.bookings import Booking, BookingAdd
from src.repositories.utils import rooms_ids_for_booking


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsORM)
            .filter(BookingsORM.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, data: BookingAdd, hotel_id: int, user_id: int):
        room = await RoomsRepository(self.session).get_one_or_none(id=data.room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Номера с таким id не существует")

        vacant_rooms_ids_subquery = rooms_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id
        )
        query = (
            select(RoomsORM)
            .filter(RoomsORM.id == data.room_id)
            .filter(RoomsORM.id.in_(select(vacant_rooms_ids_subquery.c.room_id)))
        )

        result = await self.session.execute(query)
        vacant_room = result.scalars().one_or_none()
        if not vacant_room:
            raise HTTPException(status_code=400, detail="Номер не доступен на выбранные даты")

        booking_data_full = BookingAdd(**data.model_dump(), user_id=user_id, price=room.price)
        return await BookingsRepository(self.session).add(booking_data_full)
