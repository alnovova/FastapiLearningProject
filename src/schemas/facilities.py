from pydantic import BaseModel, ConfigDict


class FacilitiesAdd(BaseModel):
    title: str

    model_config = ConfigDict(from_attributes=True)


class Facilities(FacilitiesAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
