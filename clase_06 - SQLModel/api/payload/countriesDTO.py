from models.users import CountryBase
from sqlmodel import SQLModel


class CountryResponse(CountryBase):
    id: int


class CreateCountryRequest(CountryBase):
    pass


class CreateCountryResponse(SQLModel):
    id: int
    name: str


class GetCountriesResponse(SQLModel):
    id: int
    name: str

class GetCountryByIdResponse(SQLModel):
    name:str