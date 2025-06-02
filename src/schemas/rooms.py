from pydantic import BaseModel, Field, ConfigDict


class RoomBase(BaseModel):
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class RoomAdd(RoomBase):
    hotel_id: int


class Room(RoomAdd):
    id: int


class RoomPatch(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)

    model_config = ConfigDict(from_attributes=True)
