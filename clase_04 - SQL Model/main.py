# Comando para ejecutar el servidor:
# python -m uvicorn main:app --reload 
# (Asumiendo que el archivo se llama main.py)

from typing import Annotated, Sequence
# Herramientas de FastAPI para la API, dependencias, errores y parámetros web
from fastapi import Depends, FastAPI, HTTPException, Query
# Herramientas de SQLModel para crear modelos, conectar y consultar la base de datos
from sqlmodel import Field, SQLModel, Session, create_engine, select


# ==========================================
# 1. DEFINICIÓN DEL MODELO DE DATOS
# ==========================================

class Country(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)

# SQLModel, al tener table=True, actúa como un modelo de datos (Pydantic) 
# y como una tabla real en la base de datos (SQLAlchemy).
class User(SQLModel, table=True):
    # primary_key=True indica que este es el identificador único. 
    # Es None por defecto porque la base de datos lo asigna automáticamente al crearlo.
    id: int | None = Field(default=None, primary_key=True)
    # index=True agiliza las búsquedas cuando consultemos por el nombre.
    name: str = Field(index=True)
    age: int
    country_id: int | None = Field(default=None, foreign_key="country.id")


# ==========================================
# 2. CONFIGURACIÓN DE LA BASE DE DATOS
# ==========================================

sqlite_file_name = "database.db"
# Cadena de conexión típica para SQLite
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=False es necesario en SQLite con FastAPI para evitar 
# errores cuando múltiples peticiones web ocurren al mismo tiempo.
connect_args = {"check_same_thread": False}
# El 'engine' es el motor que gestiona la comunicación real con el archivo de la base de datos.
engine = create_engine(sqlite_url, connect_args=connect_args)


# ==========================================
# 3. FUNCIONES DE INICIALIZACIÓN (SETUP)
# ==========================================

def create_db_and_tables():
    # Lee todas las clases que hereden de SQLModel con table=True 
    # y crea las tablas físicas en el archivo SQLite.
    SQLModel.metadata.create_all(engine)


def create_dummy_data():
    # Abre una conexión temporal para insertar datos
    with Session(engine) as session:
        # Si ya existe al menos un usuario en la tabla, detenemos la función (ya hay datos)
        if session.exec(select(User)).first():
            return
        
        # Datos de prueba
        names_ages_countries = [
            ("Martina Gómez", 28,1),
            ("Santiago Fernández", 34,3),
            ("Valentina López", 22,1),
            ("Mateo Rodríguez", 45,2),
            ("Camila Martínez", 19,2),
            ("Lucas Pérez", 31,3),
            ("Sofía García", 27,1),
            ("Nicolás Sánchez", 40,3),
            ("Julieta Díaz", 24,2),
            ("Tomás Romero", 37,1),
        ]

        
        # Convertimos las tuplas en objetos del modelo User
        users = [User(name=name, age=age, country_id=country) for name, age, country in names_ages_countries]
        session.add_all(users)
        session.commit()

        countries = [
            (1,"Argentina"),
            (2,"Brasil"),
            (3,"Chile")
        ]
        countries = [Country(name=name,id=id) for name, id in countries]
        session.add_all(countries) # session.add_all() prepara múltiples registros para ser insertados
        session.commit() # session.commit() es lo que realmente impacta (guarda) los cambios en la base de datos
        
        


# ==========================================
# 4. INYECCIÓN DE DEPENDENCIAS
# ==========================================

def get_session():
    # Crea una sesión por cada petición web. 
    # yield entrega la sesión a la ruta, y al terminar la ruta, cierra la conexión (gracias al 'with').
    with Session(engine) as session:
        yield session

# Creamos un alias. Cada vez que pongamos 'SessionDep' en una ruta, 
# FastAPI ejecutará get_session() automáticamente.
SessionDep = Annotated[Session, Depends(get_session)]


# ==========================================
# 5. CREACIÓN DE LA APLICACIÓN FASTAPI
# ==========================================

app = FastAPI()

# Este evento se ejecuta una sola vez, justo antes de que la API comience a aceptar peticiones.
@app.on_event("startup")
def on_startup():
    create_db_and_tables() # Crea el archivo y las tablas
    create_dummy_data()   # Si está vacío, le inyecta los 10 usuarios de prueba


# ==========================================
# 6. ENDPOINTS (RUTAS DE LA API)
# ==========================================

# RUTA POST: Para crear un nuevo usuario
@app.post("/user")
def create_user(user: User, session: SessionDep) -> User:
    # Agrega el usuario (recibido en formato JSON y validado) a la sesión
    session.add(user)
    # Guarda los cambios en la base de datos
    session.commit()
    # Refresca el objeto 'user' en Python para obtener el 'id' que la base de datos le acaba de asignar
    session.refresh(user)
    return user


# RUTA GET: Para listar usuarios (con paginación)
@app.get("/user")
def get_user(
    session: SessionDep,
    offset: int = 0, # ¿Cuántos registros nos saltamos? (Por defecto 0)
    # 'limit' indica cuántos devolver. Validamos con Query(le=100) que el máximo sea 100.
    limit: Annotated[int, Query(le=100)] = 100, 
) -> Sequence[User]:
    
    # Construye la consulta SQL con los límites de paginación y la ejecuta (.all() trae todos los resultados)
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


# RUTA GET: Para buscar un usuario específico por su ID
@app.get("/user/{user_id}")
def get_user_by_id(user_id: int, session: SessionDep) -> User:
    # session.get() es una forma optimizada de buscar un registro por su Primary Key (ID)
    user = session.get(User, user_id)
    
    # Si el usuario no existe (es None), lanzamos un error 404
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user

@app.get("/user/search/{name}")
def search_user(name: str, session: SessionDep) -> Sequence[User]:
    # .contains() ignora si le falta el apellido y permite búsquedas parciales
    statement = select(User).where(User.name.contains(name))
    result = session.exec(statement)
    return result.all()

@app.get("/user_mayores")
def search_mayores(session: SessionDep) -> Sequence[User]:
    # Compara directamente la columna age usando el operador >
    statement = select(User).where(User.age > 18)
    result = session.exec(statement)
    return result.all()