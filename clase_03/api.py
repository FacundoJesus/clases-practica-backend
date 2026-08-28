# Instalar antes: pip install FastApi
# Para correr la FastApi: python -m uvicorn api:app --reload
from fastapi import FastAPI
from models.users import User
from pydantic import BaseModel, ValidationError
from typing import List
from models.users import User, GetUsersResponse, CreateUserResponse

app = FastAPI()

# Array de usuarios
users = []


# Obtener todos los usuarios
@app.get("/users")
def get_all_users() -> GetUsersResponse:
    r = GetUsersResponse(users= users)
    return r

# Crear usuario
@app.post("/users")
def create_user(user: User) -> CreateUserResponse:
    # FastAPI ya validó automáticamente que los datos cumplan con el modelo 'User'
    
    # Aquí simularías guardar los datos en una base de datos.
    users.append(user)

    # Por ahora, simplemente devolvemos un mensaje de éxito con los datos recibidos.
    return {
        "message": "Usuario creado con éxito"
    }

@app.delete("/users/{id}")
def delete_user(id: int):
    for user in users:
        if user.id == id:
            users.remove(user)
            return {"message":"Usuario Eliminado"}
    return {"message":"Usuario No encontrado"}






