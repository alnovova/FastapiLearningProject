from sqlalchemy import select, insert


class BaseRepository:

    model = None


    def __init__(self, session):
        self.session = session


    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)

        return result.scalars().all()


    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)

        return result.scalars().one_or_none()

    async def add(self, data):
        stmt = insert(self.model).values(**data.model_dump()).returning(*self.model.__table__.columns)
        result = await self.session.execute(stmt)
        row = result.fetchone()
        return dict(row._mapping) if row else None
