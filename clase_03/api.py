# Instalar antes: pip install FastApi
# Para correr la FastApi: python -m uvicorn api:app --reload
from fastapi import FastAPI, status, HTTPException
from models.users import User
from models.users import User, GetUsersResponse, CreateUserResponse, DeleteUserResponse

app = FastAPI()

# Array de usuarios
users = []


# Obtener todos los usuarios
@app.get("/users")
def get_all_users() -> GetUsersResponse:
    r = GetUsersResponse(users= users)
    return r

# Crear usuario
# Crear sin repetir id
# si existe devolver excepcion
@app.post("/users")
def create_user(user: User) -> CreateUserResponse:
    
    # Aquí simularías guardar los datos en una base de datos.
    users.append(user)

    # Por ahora, simplemente devolvemos un mensaje de éxito con los datos recibidos.
    return {
        "message": "Usuario created successfully"
    }

@app.delete("/users/{id}")
def delete_user(id: int) -> DeleteUserResponse:
    # El id deberia ser un request
    for user in users:
        if user.id == id:
            users.remove(user)
            return {"message":"User deleted successfully"}
        
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "User not found"
    )

# Agregar actualizar 

# Obtener usuarios activos

# Obtener usuarios inactivos





