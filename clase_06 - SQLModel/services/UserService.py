from models.users import User
from typing import Annotated, Sequence
from abc import ABC, abstractmethod
from fastapi import Depends
from models.users import UserDB
from api.payload.usersDTO import CreateUserRequest, UpdateUserRequest
from repositories.UserRepository import UserRepository

# Inyecto dependencia de repositorio
UserRepositoryDep = Annotated[UserRepository, Depends(UserRepository)]

# Interface de servicio
class UserServiceInterface(ABC):
    @abstractmethod
    def create_user(self, user: User) -> UserDB:
        pass
    @abstractmethod
    def get_users(self, offset: int, limit: int) -> Sequence[UserDB]:
        pass
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> UserDB | None:
        pass
    @abstractmethod
    def get_user_by_name(self, name: str) -> Sequence[UserDB]:
        pass
    @abstractmethod
    def get_adult_users(self) -> Sequence[UserDB]:
        pass
    @abstractmethod
    def delete_user_by_id(self, user_id: int):
        pass
    @abstractmethod
    def update_user(self, user_id: int, user: User) -> UserDB | None:
        pass


class UserService(UserServiceInterface):
    def __init__(self, repo: UserRepositoryDep):
        self.repo = repo

    def create_user(self, user: User) -> UserDB:
        return self.repo.create_user(user)

    def get_users(self, offset: int, limit: int) -> Sequence[UserDB]:
        return self.repo.get_all(offset, limit)

    def get_user_by_id(self, user_id: int) -> UserDB | None:
        return self.repo.get_by_id(user_id)

    def get_user_by_name(self, name: str) -> Sequence[UserDB]:
        return self.repo.get_by_name(name)

    def get_adult_users(self) -> Sequence[UserDB]:
        return self.repo.get_adults()

    def delete_user_by_id(self, user_id: int):
        return self.repo.delete(user_id)

    def update_user(self, user_id: int, user: User) -> UserDB | None:
        return self.repo.update_user(user_id, user=user)