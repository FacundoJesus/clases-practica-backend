from collections.abc import Sequence
from typing import Annotated

from api.payload.users import (
    CreateUserRequest,
    CreateUserResponse,
    GetUsersResponse,
    GetUserWithCountryResponse,
    UpdateUserRequest,
)
from fastapi import APIRouter, HTTPException, Query
from models.users import User
from repositories.database import SessionDep

# Importamos el nuevo servicio
from services import UserService as userService

router = APIRouter()

# Crear usuario
@router.post("/user", response_model=CreateUserResponse)
def create_user(req: CreateUserRequest, session: SessionDep) -> User:
    return userService.createUser(session, req)

# Obtener todos los usuarios
@router.get("/user", response_model=Sequence[GetUsersResponse])
def get_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> Sequence[User]:
    return userService.getUsers(session, offset, limit)

# Buscar usuario por Id
@router.get("/user/{user_id}", response_model=GetUserWithCountryResponse)
def getUserById(user_id: int, session: SessionDep) -> User:
    user = userService.getUserById(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Buscar usuario por Nombre
@router.get("/user/search/{name}")
def getUserByName(name: str, session: SessionDep) -> Sequence[User]:
    return userService.getUserByName(session, name)

# Obtener usuarios mayores
@router.get("/user_mayores")
def getAdultUsers(session: SessionDep) -> Sequence[User]:
    return userService.getAdultUsers(session)

# Eliminar usuario
@router.delete("/user/{user_id}")
def deleteUserById(user_id: int, session: SessionDep):
    deleted = userService.deleteUserById(session, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": f"User {user_id} deleted successfully"}

# Actualizar usuario
@router.put("/user/{user_id}", response_model=GetUserWithCountryResponse)
def updateUser(user_id: int, req: UpdateUserRequest, session: SessionDep) -> User:
    user = userService.updateUser(session, user_id, req)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user