from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep, PaginationDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

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
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Номера с таким id не существует")

    booking = await db.bookings.add_booking(booking_data, hotel_id=room.hotel_id, user_id=user_id)
    await db.commit()
    return {"status": "OK", "data": booking}
