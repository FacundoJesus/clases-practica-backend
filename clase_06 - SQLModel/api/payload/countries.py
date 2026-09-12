from models.User import CountryBase
from sqlmodel import SQLModel


class CountryResponse(CountryBase):
    id: int

class CreateCountryRequest(CountryBase):
    pass

class CreateCountryResponse(SQLModel):
    name:str