from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date

    model_config = ConfigDict(from_attributes=True)


class BookingAdd(BookingAddRequest):
    user_id: int
    price: int


class Booking(BookingAdd):
    id: int
