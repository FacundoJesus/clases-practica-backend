# Importaciones
from typing import Annotated, Optional, Sequence
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import (
    Field,
    Relationship,
    Session,
    SQLModel,
    col,
    create_engine,
    select,
)

# Modelos Base (Esquemas comunes)
class CountryBase(SQLModel):
    name: str = Field(index=True)

class UserBase(SQLModel):
    name: str = Field(index=True)
    age: int
    country_id: int | None = Field(default=None, foreign_key="country.id")


# Tablas BBDD (Entidades)
# Definimos Country primero para que User pueda referenciarla sin problemas
class Country(CountryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    users: list["User"] = Relationship(back_populates="country")

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    country: Optional[Country] = Relationship(back_populates="users")


# DTOs de Entrada (Creación)
class UserCreate(UserBase):
    pass


# DTOs de Salida (Respuestas públicas)
class CountryPublic(CountryBase):
    id: int

class UserPublic(UserBase):
    id: int

class UserPublicWithCountry(UserPublic):
    country: CountryPublic | None = None


# Configuración de la Base de Datos
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


# Inicialización y Datos de Prueba
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_dummy_data():
    with Session(engine) as session:
        if session.exec(select(User)).first():
            return
        country_names = [("Argentina", 1), ("Brasil", 2)]
        countries = [Country(name=name, id=id) for name, id in country_names]

        session.add_all(countries)
        session.commit()

        names_and_ages = [
            ("Martina Gómez", 28, 1),
            ("Santiago Fernández", 34, 1),
            ("Valentina López", 22, 1),
            ("Mateo Rodríguez", 45, 1),
            ("Camila Martínez", 19, 2),
            ("Lucas Pérez", 31, 2),
            ("Sofía García", 27, 2),
            ("Nicolás Sánchez", 40, 2),
            ("Julieta Díaz", 24, 2),
            ("Tomás Romero", 37, 2),
        ]
        users = [User(name=name, age=age, country_id=country) for name, age, country in names_and_ages]
        session.add_all(users)
        session.commit()


# Inyección de Dependencias
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

# Configuración de la App y Evento de Inicio
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    create_dummy_data()


# Rutas (Endpoints) de la API
@app.post("/user", response_model=UserPublic)
def create_user(user: UserCreate, session: SessionDep) -> User:
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get("/user", response_model=Sequence[UserPublicWithCountry])
def get_user(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> Sequence[User]:
    statement = select(User).offset(offset).limit(limit)
    result = session.exec(statement)
    return result.all()

@app.get("/user/{user_id}", response_model=UserPublicWithCountry)
def get_user_by_id(user_id: int, session: SessionDep) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/user/search/{name}", response_model=Sequence[UserPublicWithCountry])
def search_user(name: str, session: SessionDep) -> Sequence[User]:
    statement = select(User).where(col(User.name).like(f"%{name}%"))
    result = session.exec(statement)
    return result.all()

@app.get("/user_mayores", response_model=Sequence[UserPublicWithCountry])
def search_mayores(session: SessionDep) -> Sequence[User]:
    statement = select(User).where(User.age >= 18)
    result = session.exec(statement)
    return result.all()

@app.delete("/user/{user_id}", response_model=UserPublic)
def delete_user(user_id:int, session: SessionDep) -> UserPublic:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not exist")

    # Congelamos los datos en el DTO antes de borrarlo de la base de datos
    user_deleted = UserPublic.model_validate(user)

    session.delete(user)
    session.commit()

    return user_deleted