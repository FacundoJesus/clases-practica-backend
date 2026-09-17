from collections.abc import Sequence
from typing import Annotated

from api.payload.usersDTO import (
    CreateUserRequest,
    CreateUserResponse,
    GetUsersResponse,
    GetUserWithCountryResponse,
    UpdateUserRequest,
)
from fastapi import APIRouter, HTTPException, Query, Depends
from models.users import User, UserDB
from services.UserService import UserServiceInterface,UserService

# Inyecto dependencia de servicio
UserServiceDep = Annotated[UserServiceInterface, Depends(UserService)]

router = APIRouter()

# Crear usuario
@router.post("/user", response_model=CreateUserResponse)
def create_user(userRequest: CreateUserRequest, service: UserServiceDep) -> UserDB:
    return service.createUser(userRequest)

# Obtener todos los usuarios
@router.get("/user", response_model=Sequence[GetUsersResponse])
def get_users(
    service: UserServiceDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
) -> Sequence[UserDB]:
    return service.getUsers(offset, limit)

# Buscar usuario por Id
@router.get("/user/{user_id}", response_model=GetUserWithCountryResponse)
def getUserById(user_id: int, service: UserServiceDep) -> UserDB:
    user = service.getUserById(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Buscar usuario por Nombre
@router.get("/user/search/{name}")
def getUserByName(name: str, service: UserServiceDep) -> Sequence[UserDB]:
    return service.getUserByName(name)

# Obtener usuarios mayores
@router.get("/user_mayores")
def getAdultUsers(service: UserServiceDep) -> Sequence[UserDB]:
    return service.getAdultUsers()

# Eliminar usuario
@router.delete("/user/{user_id}", response_model=dict[str, str])
def deleteUserById(user_id: int, service: UserServiceDep) -> dict[str, str]:
    deleted = service.deleteUserById(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": f"User {user_id} deleted successfully"}

# Actualizar usuario
@router.put("/user/{user_id}", response_model=GetUserWithCountryResponse)
def updateUser(user_id: int, req: UpdateUserRequest, service: UserServiceDep) -> UserDB:
    user = service.updateUser(user_id, req)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Quitar país asociado al usuario
@router.patch("/user/{user_id}/remove_country", response_model=GetUserWithCountryResponse)
def removeUserCountry(user_id: int, service: UserService = Depends()) -> UserDB:
    """Remueve el país asociado a un usuario por su ID."""
    user = service.removeUserCountry(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user