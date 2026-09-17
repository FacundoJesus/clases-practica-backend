from typing import Annotated, Sequence

from fastapi import Depends, Query

from repositories.UserRepository import UserRepository
from models.users import User
from api.payload.usersDTO import CreateUserRequest, UpdateUserRequest

UserRepositoryDep = Annotated[UserRepository, Depends(UserRepository)]

class UserService:
    def __init__(self, repo: UserRepositoryDep):
        self.repo = repo

    def createUser(self, req: CreateUserRequest) -> User:
        user = User(name=req.name, age=req.age, country_id=req.country_id,password=req.password)
        return self.repo.save(user)

    def removeUserCountry(self, user_id: int) -> User | None:
        """Remueve el país asociado a un usuario por su ID."""
        user = self.repo.get_by_id(user_id)
        if not user:
            return None
        
        user.country_id = None
        return self.repo.save(user)

    def getUsers(self, offset: int, limit: int) -> Sequence[User]:
        return self.repo.get_all(offset, limit)

    def getUserById(self, user_id: int) -> User | None:
        return self.repo.get_by_id(user_id)

    def getUserByName(self, name: str) -> Sequence[User]:
        return self.repo.get_by_name(name)

    def getAdultUsers(self) -> Sequence[User]:
        return self.repo.get_adults()

    def deleteUserById(self, user_id: int) -> bool:
        user = self.repo.get_by_id(user_id)
        if not user:
            return False # Retorna Falso si el usuario no existe
        
        self.repo.delete(user)
        return True # Retorna Verdadero si se eliminó con éxito

    def updateUser(self, user_id: int, req: UpdateUserRequest) -> User | None:
        user = self.repo.get_by_id(user_id)
        if not user:
            return None # Retorna None si no existe
        
        # Extraemos solo los datos que el usuario envió en la petición HTTP
        update_data = req.model_dump(exclude_unset=True) 
        
        # Actualizamos los atributos del modelo User dinámicamente
        for key, value in update_data.items():
            setattr(user, key, value)
            
        return self.repo.save(user)