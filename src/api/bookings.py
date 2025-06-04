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

    overlapping = await db.bookings.get_overlapping(
        room_id=booking_data.room_id,
        date_from=booking_data.date_from,
        date_to=booking_data.date_to
    )
    if overlapping:
        raise HTTPException(status_code=400, detail="Номер уже забронирована на выбранные даты")

    booking_data_full = BookingAdd(**booking_data.model_dump(), user_id=user_id, price=room.price)
    booking = await db.bookings.add(booking_data_full)
    await db.commit()

    return {"status": "OK", "data": booking}
