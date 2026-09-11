from collections.abc import Sequence
from typing import Annotated

from api.payload.users import (
    CreateUserRequest,
    CreateUserResponse,
    GetUserResponseWithCountry,
    GetUsersResponse,
)
from fastapi import APIRouter, HTTPException, Query
from models.user import User
from repositories.database import SessionDep
from sqlmodel import col, select

router = APIRouter()

# Crear usuario
@router.post("/user", response_model=CreateUserResponse)
def create_user(req: CreateUserRequest, session: SessionDep) -> User:
    user = User(name=req.name, age=req.age, country_id=req.country_id)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Obtener todos los usuarios
@router.get("/user", response_model=Sequence[GetUsersResponse])
def get_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
)-> Sequence[User]:
    statement = select(User).offset(offset).limit(limit)
    result = session.exec(statement)
    users = result.all()
    return users

# Buscar usuario por Id
@router.get("/user/{user_id}", response_model=GetUserResponseWithCountry)
def get_user_by_id(user_id: int, session: SessionDep) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Buscar usuario por Nombre
@router.get("/user/search/{name}")
def search_user(name: str, session: SessionDep) -> Sequence[User]:
    statement = select(User).where(col(User.name).like(f"%{name}%"))
    result = session.exec(statement)
    return result.all()

# Obtener usuarios mayores
@router.get("/user_mayores")
def search_mayores(session: SessionDep)-> Sequence[User]:
    # TODO: users.age >= 18
    statement = select(User).where(User.age >= 18)
    result = session.exec(statement)
    return result.all()
