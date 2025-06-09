from datetime import date

from fastapi import APIRouter, Query, HTTPException

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms/", summary="Получение номеров")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2025-05-30"),
        date_to: date = Query(example="2025-06-12")
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение номера")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms/", summary="Добавление номера")
async def create_room(
        hotel_id: int,
        db: DBDep,
        room_data: RoomAddRequest
):
    room_data_full = RoomAdd(**room_data.model_dump(), hotel_id=hotel_id)
    room = await db.rooms.add(room_data_full)
    if room_data.facilities_ids:
        rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
        await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменение номера")
async def edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest,
        db: DBDep
):
    room = await db.rooms.get_one_or_none(id=room_id)
    if not room:
        raise HTTPException(404, "Номер не найден")
    room_data_full = RoomAdd(**room_data.model_dump(), hotel_id=hotel_id)
    await db.rooms.edit(data=room_data_full, hotel_id=hotel_id, id=room_id)
    await db.rooms_facilities.set_room_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()
    return {"status": "OK", "data": room}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное изменение номера")
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
        db: DBDep
):
    room_data_dict = room_data.model_dump(exclude_unset=True)
    room_data_full = RoomPatch(**room_data_dict, hotel_id=hotel_id)
    await db.rooms.edit(data=room_data_full, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    if "facilities_ids" in room_data_dict:
        await db.rooms_facilities.set_room_facilities(room_id=room_id, facilities_ids=room_data_dict["facilities_ids"])
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}
