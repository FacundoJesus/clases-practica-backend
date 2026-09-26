from pydantic import EmailStr
from sqlmodel import SQLModel


class LoginRequest(SQLModel):
    email: EmailStr
    password: str

class LoginResponse(SQLModel):
    msg: str
    token: str