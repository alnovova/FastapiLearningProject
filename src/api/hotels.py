from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPatch, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение отелей")
@cache(expire=10)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        date_from: date = Query(examples=["2025-05-30"]),
        date_to: date = Query(examples=["2025-06-12"]),
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Адрес")
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        limit=pagination.per_page,
        offset=per_page * (pagination.page - 1),
        date_from=date_from,
        date_to=date_to,
        title=title,
        location=location
    )


@router.get("/{hotel_id}", summary="Получение отеля")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("", summary="Добавление отеля")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples={
            "1": {"summary": "Сочи", "value": {
                "title": "Отель 5 звезд у моря",
                "location": "sochi",
            }},
            "2": {"summary": "Дубай", "value": {
                "title": "Отель",
                "location": "dubai",
            }}
        }),
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Изменение отеля")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit(data=hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное изменения отеля")
async def partially_edit_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await db.hotels.edit(data=hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}
