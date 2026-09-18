from .countriesDTO import CountryResponse
from sqlmodel import SQLModel


class CreateUserRequest(SQLModel):
    name: str
    age: int
    country_id: int | None
    password: str

class CreateUserResponse(SQLModel):
    id: int

class GetUsersResponse(SQLModel):
    id: int
    name: str

class GetUserWithCountryResponse(GetUsersResponse):
    age: int
    password: str | None
    country: CountryResponse | None = None

class UpdateUserRequest(SQLModel):
    name: str 
    age: int 
    country_id: int | None

class DeleteUserResponse(SQLModel):
    msj:str
