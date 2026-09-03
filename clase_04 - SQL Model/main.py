# Comando para ejecutar el servidor:
# python -m uvicorn main:app --reload 
# (Asumiendo que el archivo se llama main.py)

from typing import Annotated, List
from fastapi import Depends, FastAPI, Query
from sqlmodel import Field, SQLModel, Session, create_engine, select

# 1. DEFINICIÓN DEL MODELO
# SQLModel combina Pydantic (validación de datos para la API) y SQLAlchemy (tablas de BD).
# table=True indica que esta clase creará una tabla real en la base de datos.
class User(SQLModel, table=True):
    # primary_key=True lo define como identificador único. default=None permite que la BD autogenere el ID.
    id: int | None = Field(default=None, primary_key=True)
    # index=True agiliza las búsquedas por nombre en la base de datos.
    name: str = Field(index=True)


# 2. CONFIGURACIÓN DE LA BASE DE DATOS
sqlite_file_name = "database.db" # Nombre del archivo local que se creará.
sqlite_url = f"sqlite:///{sqlite_file_name}" # URL de conexión.

# check_same_thread=False es necesario en SQLite cuando se usa con frameworks asíncronos como FastAPI.
connect_args = {"check_same_thread": False}
# El 'engine' es el motor que gestiona la comunicación entre tu código y SQLite.
engine = create_engine(sqlite_url, connect_args=connect_args)


# 3. FUNCIONES DE BASE DE DATOS
def create_db_and_tables():
    # Lee todas las clases que heredan de SQLModel (como User) y crea las tablas si no existen.
    SQLModel.metadata.create_all(engine)

def get_session():
    # Crea una sesión con la BD. 'yield' pausa la función, entrega la sesión al endpoint, 
    # y la cierra automáticamente cuando el endpoint termina.
    with Session(engine) as session:
        yield session

# SessionDep es un alias. FastAPI inyectará la sesión automáticamente (Dependency Injection)
# cada vez que un endpoint pida este tipo de dato.
SessionDep = Annotated[Session, Depends(get_session)]


# 4. INICIALIZACIÓN DE LA APLICACIÓN
app = FastAPI()

# Este evento se dispara justo antes de que el servidor empiece a recibir peticiones.
@app.on_event("startup")
def on_startup():
    create_db_and_tables() # Nos aseguramos de que la BD y tablas existan al arrancar.


# 5. RUTAS (ENDPOINTS)
# POST: Usado para crear o enviar datos nuevos.
@app.post("/user")
def create_user(user: User, session: SessionDep) -> User:
    # Agrega el usuario a la sesión (aún no se guarda en disco).
    session.add(user)
    # Ejecuta los cambios en la base de datos (lo guarda permanentemente).
    session.commit()
    # Actualiza el objeto 'user' con los datos generados por la BD (ej. el 'id' autogenerado).
    session.refresh(user)
    return user

# GET: Usado para consultar o leer datos.
@app.get("/user")
def get_user(
    session: SessionDep,
    offset: int = 0, # Para paginación: cuántos registros saltarse.
    # le=100 (less or equal) limita la consulta a 100 resultados máximo por seguridad.
    limit: Annotated[int, Query(le=100)] = 100,
) -> List[User]:
    # select(User) arma la consulta. offset y limit aplican la paginación. 
    # session.exec() la ejecuta y .all() trae todos los resultados en una lista.
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users