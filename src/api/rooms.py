from fastapi import APIRouter, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms/", summary="Получение номеров")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение номера")
async  def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms/", summary="Добавление номера")
async def create_room(
        hotel_id: int,
        room_data: RoomAddRequest = Body(openapi_examples={
            "1": {"summary": "С описанием", "value": {
                "title": "Люкс на двоих",
                "description": "Просторный и уютный номер с улучшенной планировкой, идеально подходящий для комфортного размещения пары",
                "price": "70000",
                "quantity": "3",
            }},
            "2": {"summary": "Без описания", "value": {
                "title": "Номер на двоих",
                "price": "15000",
                "quantity": "20",
            }}
        })
):
    room_data_full = RoomAdd(**room_data.model_dump(), hotel_id=hotel_id)

    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data_full)
        await session.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменение номера")
async def edit_hotel(
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest
):
    room_data_full = RoomAdd(**room_data.model_dump(), hotel_id=hotel_id)

    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=room_data_full, hotel_id=hotel_id, id=room_id)
        await session.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное изменение номера")
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest
):
    room_data_full = RoomPatch(**room_data.model_dump(exclude_unset=True), hotel_id=hotel_id)

    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=room_data_full, exclude_unset=True, hotel_id=hotel_id, id=room_id)
        await session.commit()

    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()

    return {"status": "OK"}
