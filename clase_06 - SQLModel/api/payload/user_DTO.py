from .country_DTO import CountryResponse
from pydantic import EmailStr
from sqlmodel import SQLModel, Field


#Nivel API
class CreateUserRequest(SQLModel):
    name: str
    age: int
    country_id: int | None
    email: EmailStr
    password: str = Field(max_length=10, min_length=4)

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
    email: EmailStr
    password: str = Field(max_length=10, min_length=4)

class DeleteUserResponse(SQLModel):
    msj:str
