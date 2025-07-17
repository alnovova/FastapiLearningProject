from datetime import date

from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    fields = {
        "user_id": user_id,
        "room_id": room_id,
        "date_from": date(year=2023, month=12, day=30),
        "date_to": date(year=2024, month=1, day=1),
        "price": 100,
    }

    booking_data_for_add = BookingAdd(**fields)
    new_booking = await db.bookings.add(booking_data_for_add)
    new_booking_id = new_booking.id
    new_booking_data = new_booking.model_dump()
    assert set(fields.items()).issubset(set(new_booking_data.items())), (
        f"Несовпадения: {fields.items() - new_booking_data.items()}"
    )

    fields["date_to"] = date(year=2024, month=1, day=10)
    fields["price"] = 200
    booking_data_for_update = BookingAdd(**fields)
    await db.bookings.edit(booking_data_for_update, id=new_booking_id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking_id)
    updated_booking_data = updated_booking.model_dump()
    assert set(fields.items()).issubset(set(updated_booking_data.items())), (
        f"Несовпадения: {fields.items() - updated_booking_data.items()}"
    )

    await db.bookings.delete(id=new_booking_id)
    assert not await db.bookings.get_one_or_none(id=new_booking_id)

    await db.rollback()
