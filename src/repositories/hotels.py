from sqlalchemy import select

from src.models.hotels import HotelsORM
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):

    model = HotelsORM


    async def get_all(self, title, location, limit, offset):
        query = select(HotelsORM)
        if title:
            query = query.filter(HotelsORM.title.ilike(f"%{title}%"))
        if location:
            query = query.filter(HotelsORM.location.ilike(f"%{location}%"))
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)

        hotels = result.scalars().all()

        return hotels
