from .countries import CountryResponse
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
    name: str | None = None
    age: int | None = None
    country_id: int | None = None


