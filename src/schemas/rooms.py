from pydantic import BaseModel, ConfigDict


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class RoomAdd(RoomAddRequest):
    hotel_id: int


class Room(RoomAdd):
    id: int


class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None

    model_config = ConfigDict(from_attributes=True)


class RoomPatch(RoomPatchRequest):
    hotel_id: int