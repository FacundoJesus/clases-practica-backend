# Instalar antes en terminal: pip install pydantic
# Instalar antes : pip install 'pydantic[email]'
from pydantic import BaseModel, EmailStr, Field, HttpUrl,field_validator
from typing import List

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    apellido: str = Field(min_length=4)
    edad: int = Field(gt=18, lt=30)  
    cuil: int
    isActive: bool = True

    # Usamos field_validator apuntando al campo 'cuil'
    @field_validator('cuil')
    @classmethod
    def cuil_validator(cls, v: int):
        # Convertimos a string para contar los dígitos fácilmente
        if len(str(v)) != 11:
            raise ValueError('El CUIL debe tener exactamente 11 dígitos')
        # Siempre debes retornar el valor si pasa la validación
        return v


class GetUsersResponse(BaseModel):
    users: List[User]

class CreateUserResponse(BaseModel):
    message:str
    user:User

class DeleteUserResponse(BaseModel):
    message:str

class UpdateeUserResponse(BaseModel):
    message:str
    user:User
