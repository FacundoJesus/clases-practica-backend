from collections.abc import Sequence
from api.payload.usersDTO import CreateUserRequest, UpdateUserRequest
from models.users import User
from sqlmodel import col, select
from repositories.database import SessionDep

class UserService:
    def __init__(self, session: SessionDep):
        self.session = session

    def createUser(self, req: CreateUserRequest) -> User:
        user = User(name=req.name, age=req.age, country_id=req.country_id)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def removeUserCountry(self, user_id: int) -> User | None:
        """Remueve el país asociado a un usuario por su ID."""
        user = self.session.get(User, user_id)
        if not user:
            return None
        
        user.country_id = None
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def getUsers(self, offset: int, limit: int) -> Sequence[User]:
        statement = select(User).offset(offset).limit(limit)
        return self.session.exec(statement).all()

    def getUserById(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)

    def getUserByName(self, name: str) -> Sequence[User]:
        statement = select(User).where(col(User.name).like(f"%{name}%"))
        return self.session.exec(statement).all()

    def getAdultUsers(self) -> Sequence[User]:
        statement = select(User).where(User.age >= 18)
        return self.session.exec(statement).all()

    def deleteUserById(self, user_id: int) -> bool:
        user = self.session.get(User, user_id)
        if not user:
            return False # Retorna Falso si el usuario no existe
        
        self.session.delete(user)
        self.session.commit()
        return True # Retorna Verdadero si se eliminó con éxito

    def updateUser(self, user_id: int, req: UpdateUserRequest) -> User | None:
        user = self.session.get(User, user_id)
        if not user:
            return None # Retorna None si no existe
        
        # Extraemos solo los datos que el usuario envió en la petición HTTP
        update_data = req.model_dump(exclude_unset=True) 
        
        # Actualizamos los atributos del modelo User dinámicamente
        for key, value in update_data.items():
            setattr(user, key, value)
            
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user