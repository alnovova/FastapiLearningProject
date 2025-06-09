from pydantic import BaseModel, ConfigDict

from src.schemas.facilities import Facility


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = []


class RoomAdd(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    hotel_id: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomWithRels(Room):
    facilities: list[Facility]


class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] | None = None


class RoomPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    hotel_id: int

    model_config = ConfigDict(from_attributes=True)
