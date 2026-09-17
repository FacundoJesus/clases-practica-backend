from typing import Annotated, Sequence
from abc import ABC, abstractmethod
from fastapi import Query
from sqlmodel import select, col

from repositories.database import SessionDep
from models.users import UserDB

# Interface de repositorio
class UserRepositoryInterface(ABC):
    @abstractmethod
    def save(self, user: UserDB) -> UserDB:
        pass
    @abstractmethod
    def get_all(self, offset: int, limit: int) -> Sequence[UserDB]:
        pass
    @abstractmethod
    def get_by_id(self, user_id: int) -> UserDB | None:
        pass
    @abstractmethod
    def get_by_name(self, name: str) -> Sequence[UserDB]:
        pass
    @abstractmethod
    def get_adults(self) -> Sequence[UserDB]:
        pass
    @abstractmethod
    def delete(self, user: UserDB) -> None:
        pass

class UserRepository(UserRepositoryInterface):
    def __init__(self, session: SessionDep):
        self.session = session

    def save(self, user: UserDB) -> UserDB:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

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

    def delete(self, user: UserDB) -> None:
        self.session.delete(user)
        self.session.commit()