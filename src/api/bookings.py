from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


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
