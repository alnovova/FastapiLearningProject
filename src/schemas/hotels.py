from pydantic import BaseModel, ConfigDict


class HotelAdd(BaseModel):
    title: str
    location: str

    model_config = ConfigDict(from_attributes=True)


class Hotel(HotelAdd):
    id: int


class HotelPatch(BaseModel):
    title: str | None = None
    location: str | None = None

    model_config = ConfigDict(from_attributes=True)
