from typing import Annotated, Sequence

from fastapi import Query
from sqlmodel import select, col

from repositories.database import SessionDep
from models.users import User


class UserRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def save(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_all(
        self,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
    )-> Sequence[User]:
        statement = select(User).offset(offset).limit(limit)
        result = self.session.exec(statement)
        users = result.all()
        return users

    def get_by_id(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)

    def get_by_name(self, name: str) -> Sequence[User]:
        statement = select(User).where(col(User.name).like(f"%{name}%"))
        return self.session.exec(statement).all()

    def get_adults(self) -> Sequence[User]:
        statement = select(User).where(User.age >= 18)
        return self.session.exec(statement).all()

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()