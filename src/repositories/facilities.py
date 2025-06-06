from src.models.facilities import FacilitiesORM
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facilities


class FacilitiesRepository(BaseRepository):

    model = FacilitiesORM
    schema = Facilities
