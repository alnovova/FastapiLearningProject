from datetime import date

from sqlalchemy import select, and_

from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsORM
    schema = Booking

    async def get_overlapping(self, room_id: int, date_from: date, date_to: date) -> list[Booking]:
        query = select(self.model).where(
            and_(
                self.model.room_id == room_id,
                self.model.date_from < date_to,
                date_from < self.model.date_to
            )
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]
