from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep, PaginationDep
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получение удобств")
async def get_facilities(pagination: PaginationDep, db: DBDep):
    per_page = pagination.per_page or 10
    return await db.facilities.get_all(offset=per_page * (pagination.page - 1))


@router.post("", summary="Добавление удобства")
async def create_facility(user_id: UserIdDep, facility_data: FacilityAdd, db: DBDep):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "OK", "data": facility}
