from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsORM
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Сочи", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Париж", "name": "paris"},
    {"id": 4, "title": "Нью Йорк", "name": "new_york"},
    {"id": 5, "title": "Токио", "name": "tokyo"},
    {"id": 6, "title": "Барселона", "name": "barcelona"},
    {"id": 7, "title": "Сидней", "name": "sydney"},
]

@router.get(
    "",
    summary="Получение отелей"
)
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Адрес")
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )



@router.delete(
    "/{hotel_id}",
    summary="Удаление отеля"
)
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post(
    "",
    summary="Добавление отеля"
)
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель 5 звезд у моря",
        "location": "sochi",
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель",
        "location": "dubai",
    }}
})):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="Изменение отеля"
)
def update_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            return {"status": "OK"}
        return {"status": "ERROR", "message": "Элемент не найден"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное изменения отеля"
)
def partially_update_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
            return {"status": "OK"}
        return {"status": "ERROR", "message": "Элемент не найден"}