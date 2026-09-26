from models.users import Country
from sqlmodel import SQLModel


class CountryResponse(Country):
    id: int


class CreateCountryRequest(Country):
    pass


class CreateCountryResponse(SQLModel):
    id: int
    name: str


class GetCountriesResponse(SQLModel):
    id: int
    name: str

class GetCountryByIdResponse(SQLModel):
    name:str

class UpdateCountryRequest(SQLModel):
    name: str | None = None