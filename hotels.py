from fastapi import Query, APIRouter, Body

from schemas.hotels import Hotel, HotelPATCH


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
def get_hotels(
        id: int | None = Query(None, description="Идентификатор"),
        title: str | None = Query(None, description="Название отеля"),
        page: int = Query(1, description="Номер страницы"),
        per_page: int = Query(3, description="Количество элементов на странице"),
):
    filtered_hotels = [
        hotel for hotel in hotels
        if (id is None or hotel["id"] == id)
           and (title is None or hotel["title"] == title)
    ]

    start = (page - 1) * per_page
    end = start + per_page
    return filtered_hotels[start:end]


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
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "name": "sochi_u_moria",
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель Дубай",
        "name": "otel_dubai",
    }}
})):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
    return {"status": "OK"}


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