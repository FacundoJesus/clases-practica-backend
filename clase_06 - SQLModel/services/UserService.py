from collections.abc import Sequence

from api.payload.users import CreateUserRequest, UpdateUserRequest
from models.user import User
from sqlmodel import Session, col, select


def createUser(session: Session, req: CreateUserRequest) -> User:
    user = User(name=req.name, age=req.age, country_id=req.country_id)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def getUsers(session: Session, offset: int, limit: int) -> Sequence[User]:
    statement = select(User).offset(offset).limit(limit)
    return session.exec(statement).all()

def getUserById(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)

def getUserByName(session: Session, name: str) -> Sequence[User]:
    statement = select(User).where(col(User.name).like(f"%{name}%"))
    return session.exec(statement).all()

def getAdultUsers(session: Session) -> Sequence[User]:
    statement = select(User).where(User.age >= 18)
    return session.exec(statement).all()

def deleteUserById(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if not user:
        return False # Retorna Falso si el usuario no existe
    
    session.delete(user)
    session.commit()
    return True # Retorna Verdadero si se eliminó con éxito

def updateUser(session: Session, user_id: int, req: UpdateUserRequest) -> User | None:
    user = session.get(User, user_id)
    if not user:
        return None # Retorna None si no existe
    
    # Extraemos solo los datos que el usuario envió en la petición HTTP
    update_data = req.model_dump(exclude_unset=True) 
    
    # Actualizamos los atributos del modelo User dinámicamente
    for key, value in update_data.items():
        setattr(user, key, value)
        
    session.add(user)
    session.commit()
    session.refresh(user)
    return user