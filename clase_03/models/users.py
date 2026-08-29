# Instalar antes en terminal: pip install pydantic
# Instalar antes : pip install 'pydantic[email]'
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List

class User(BaseModel):
    id: int
    firstName: str
    email: EmailStr
    lastName: str = Field(min_length=4)
    age: int = Field(gt=18, lt=30)  
    cuil: int
    isActive: bool = True

    # Usamos field_validator apuntando al campo 'cuil'
    @field_validator('cuil')
    @classmethod
    def cuil_validator(cls, v: int):
        # Convertimos a string para contar los dígitos fácilmente
        if len(str(v)) != 11:
            raise ValueError('The CUIL must have 11 digitis')
        # Siempre debes retornar el valor si pasa la validación
        return v


class GetUsersResponse(BaseModel):
    users: List[User]

class CreateUserResponse(BaseModel):
    message:str
    user:User

class DeleteUserResponse(BaseModel):
    message:str

class UpdateUserResponse(BaseModel):
    message:str
    user:User
