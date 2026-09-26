from typing import Annotated

from fastapi import Depends

from repositories.user_repository import UserRepository

UserRepositoryDep = Annotated[UserRepository, Depends(UserRepository)]

class LoginService():

    def __init__(self, repo: UserRepositoryDep):
        self.repo = repo

    def login(self, email: str, password: str) -> bool:
        user = self.repo.get_by_email(email)
        if not user:
            return False
        return user.password == password