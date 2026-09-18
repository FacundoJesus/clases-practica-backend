from models.users import User
from typing import Annotated, Sequence
from abc import ABC, abstractmethod
from fastapi import Query
from sqlmodel import select, col

from repositories.database import SessionDep
from models.users import UserDB

class UserRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def create_user(self, user: User) -> UserDB:
        userDb = UserDB(name=user.name, age=user.age, country_id=user.country_id)
        self.session.add(userDb)
        self.session.commit()
        self.session.refresh(userDb)
        return userDb

    def get_all(
        self,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
    )-> Sequence[UserDB]:
        statement = select(UserDB).offset(offset).limit(limit)
        result = self.session.exec(statement)
        users = result.all()
        return users

    def get_by_id(self, user_id: int) -> UserDB | None:
        return self.session.get(UserDB, user_id)

    def get_by_name(self, name: str) -> Sequence[UserDB]:
        statement = select(UserDB).where(col(UserDB.name).like(f"%{name}%"))
        return self.session.exec(statement).all()

    def get_adults(self) -> Sequence[UserDB]:
        statement = select(UserDB).where(UserDB.age >= 18)
        return self.session.exec(statement).all()

    def delete(self, user_id: int):
        user = self.session.get(UserDB, user_id)
        self.session.delete(user)
        self.session.commit()


    def update_user(self, user_id: int, user: User) -> UserDB | None:
        userDb = self.session.get(UserDB, user_id)
        if userDb:
            userDb.age = user.age
            userDb.name = user.name
            userDb.country_id = user.country_id
            self.session.add(userDb)
            self.session.commit()
            self.session.refresh(userDb)
        return userDb