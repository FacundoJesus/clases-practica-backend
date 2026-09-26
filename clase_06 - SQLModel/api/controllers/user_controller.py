from collections.abc import Sequence
from typing import Annotated
from api.payload.user_DTO import (
    CreateUserRequest,
    CreateUserResponse,
    GetUsersResponse,
    GetUserWithCountryResponse,
    UpdateUserRequest,
    DeleteUserResponse
)
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException, Header, Query
from models.users import User, UserDB
from services.user_service import UserServiceInterface, UserService


# Inyecto dependencia de servicio
UserServiceDep = Annotated[UserServiceInterface, Depends(UserService)]


def verify_api_key_header(x_api_key: Annotated[str, Header()]) -> str:
    return x_api_key

router = APIRouter(dependencies=[Depends(verify_api_key_header)],tags=["Users"])

# Crear usuario
@router.post("/user", response_model=CreateUserResponse)
def create_user(createUserReq: CreateUserRequest, service: UserServiceDep) -> UserDB:
    newUser = User(name=createUserReq.name, age=createUserReq.age, email=createUserReq.email, 
                   password=createUserReq.password, country_id=createUserReq.country_id)
    return service.create_user(newUser)

# Obtener todos los usuarios
@router.get("/user", response_model=Sequence[GetUsersResponse])
def get_users(
    service: UserServiceDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
) -> Sequence[UserDB]:
    return service.get_users(offset, limit)


# Buscar usuario por Id
@router.get("/user/{user_id}", response_model=GetUserWithCountryResponse)
def get_user_by_id(user_id: int, service: UserServiceDep) -> UserDB:
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Buscar usuario por Nombre
@router.get("/user/search/{name}")
def get_user_by_name(name: str, service: UserServiceDep) -> Sequence[UserDB]:
    return service.get_user_by_name(name)


# Obtener usuarios mayores
@router.get("/user_mayores")
def get_adult_users(service: UserServiceDep) -> Sequence[UserDB]:
    return service.get_adult_users()


# Eliminar usuario
@router.delete("/user/{user_id}", response_model=DeleteUserResponse)
def delete_user_by_id(user_id: int, service: UserServiceDep) -> DeleteUserResponse:
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    service.delete_user_by_id(user_id)
    return DeleteUserResponse(msj='Usuario borrado con éxito')


# Actualizar usuario
@router.patch("/user/{user_id}", response_model=GetUserWithCountryResponse)
def update_user(user_id: int, updateUserReq: UpdateUserRequest, service: UserServiceDep) -> UserDB:
    user = User(name=updateUserReq.name, age=updateUserReq.age, email=updateUserReq.email, 
                       password=updateUserReq.password, country_id=updateUserReq.country_id)
    response= service.update_user(user_id, user)
    if not response:
        raise HTTPException(status_code=404, detail="User not found")
    return response

