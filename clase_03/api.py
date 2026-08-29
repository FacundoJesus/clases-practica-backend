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
    return GetUsersResponse(users= users)

# Obtener Usuarios Activos
@app.get("/users/active")
def get_active_users() -> GetUsersResponse:

    activeUsers = []

    for user in users:
        if user.isActive == True:
            activeUsers.append(user)
              
    if not activeUsers:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Active users not found"
        )
    
    return GetUsersResponse(users=activeUsers)


# Obtener Usuarios Inactivos
@app.get("/users/inactive")
def get_inactive_users() -> GetUsersResponse:

    inactiveUsers = []

    for user in users:
        if user.isActive == False:
            inactiveUsers.append(user)

    if not inactiveUsers:
        raise HTTPException (
            status_code = status.HTTP_404_NOT_FOUND,
            detail= "Inactive users not found"
        )

    return GetUsersResponse(users=inactiveUsers)

# Crear usuario
# Crear sin repetir id
# si existe devolver excepcion
@app.post("/users")
def create_user(user: User) -> CreateUserResponse:
    
    users.append(user)

    return CreateUserResponse(
        message="User created successfully",
        user= user
    )

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





