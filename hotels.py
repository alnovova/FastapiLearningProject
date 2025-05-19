from fastapi import Query, Body, APIRouter


router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title":"Sochi", "name": "sochi"},
    {"id": 2, "title":"Dubai", "name": "dubai"},
]


@router.get(
    "",
    summary="Получение отелей"
)
def get_hotels(
        id: int | None = Query(None, description="Идентификатор"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    return hotels_


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
def create_hotel(
        title: str = Body(embed=True),   # embed=True обязательно прописывать, если параметр всего один
        name: str = Body(embed=True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "name": name
    })
    return {"status": "OK"}


@router.put(
    "/{hotel_id}",
    summary="Изменение отеля"
)
def update_hotel(
        hotel_id: int,
        title: str = Body(embed=True),
        name: str = Body(embed=True)
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return {"status": "OK"}
        return {"status": "ERROR", "message": "Элемент не найден"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное изменения отеля"
)
def partially_update_hotel(
        hotel_id: int,
        title: str | None = Body(None, embed=True),
        name: str | None = Body(None, embed=True)
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title is not None:
                hotel["title"] = title
            if name is not None:
                hotel["name"] = name
            return {"status": "OK"}
        return {"status": "ERROR", "message": "Элемент не найден"}