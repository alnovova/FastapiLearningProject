from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep, PaginationDep
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException
from src.schemas.bookings import BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Получение бронирований")
async def get_bookings(pagination: PaginationDep, db: DBDep):
    per_page = pagination.per_page or 10
    return await db.bookings.get_all(offset=per_page * (pagination.page - 1))


@router.get("/me", summary="Получение бронирований пользователя")
async def get_user_bookings(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("", summary="Создание бронирования")
async def create_booking(user_id: UserIdDep, booking_data: BookingAddRequest, db: DBDep):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")
    try:
        booking = await db.bookings.add_booking(booking_data, hotel_id=room.hotel_id, user_id=user_id)
    except AllRoomsAreBookedException as exc:
        raise HTTPException(status_code=409, detail=exc.detail)
    await db.commit()
    return {"status": "OK", "data": booking}
