from sqlalchemy import select, delete, insert

from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilitiesDataMapper
from src.schemas.facilities import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    mapper = FacilitiesDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    schema = RoomFacility

    async def set_room_facilities(self, room_id: int, facilities_ids: list[int]) -> None:
        get_current_facilities_ids_query = (
            select(self.model.facility_id)
            .filter_by(room_id=room_id)
        )
        result = await self.session.execute(get_current_facilities_ids_query)
        current_facilities_ids: list[int] = result.scalars().all()

        ids_to_delete: list[int] = list(set(current_facilities_ids) - set(facilities_ids))
        if ids_to_delete:
            delete_m2m_facilities_stmt = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(ids_to_delete),
                )
            )
            await self.session.execute(delete_m2m_facilities_stmt)

        ids_to_add: list[int] = list(set(facilities_ids) - set(current_facilities_ids))
        if ids_to_add:
            insert_m2m_facilities_stmt = (
                insert(self.model)
                .values([{"room_id": room_id, "facility_id":f_id} for f_id in ids_to_add])
            )
            await self.session.execute(insert_m2m_facilities_stmt)