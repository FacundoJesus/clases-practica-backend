# Para correr la FastApi: python -m uvicorn api:app --reload
from fastapi import FastAPI, status, HTTPException
from models.users import User
from models.users import User, GetUsersResponse, CreateUserResponse, DeleteUserResponse, UpdateUserResponse

app = FastAPI()

# Array de usuarios
users = []

user1 = User(
    id=1,
    name="Juan",
    apellido="Perez",       
    email="juan.perez@example.com",
    edad=25,                
    cuil=20384756291,       
    isActive=True
)
user2 = User(
    id=2,
    name="Maria",
    apellido="Gomez",       
    email="maria.gomez@example.com",
    edad=21,                
    cuil=27493827164,       
    isActive=True
)
user3 = User(
    id=3,
    name="Lucas",
    apellido="Rodriguez",   
    email="lucas.rod@example.com",
    edad=28,                
    cuil=20123456789,       
    isActive=False          
)

users.append(user1)
users.append(user2)
users.append(user3)

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
@app.post("/users")
def create_user(user: User) -> CreateUserResponse:

    for existUser in users:
        if existUser.id == user.id:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= f"User with id: {user.id} already exists."
            )
        
    users.append(user)

    return CreateUserResponse(
        message="User created successfully",
        user= user
    )

# Eliminar Usuario
@app.delete("/users/{id}")
def delete_user(id: int) -> DeleteUserResponse:
    # El id deberia ser un request
    for user in users:
        if user.id == id:
            users.remove(user)
            return DeleteUserResponse(message="User deleted successfully")
        
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "User not found"
    )


# Agregar actualizar 
@app.put("/users/{id}")
def update_user(user_id: int, user:User) -> UpdateUserResponse:

    for index, existing_user in enumerate(users):
        if existing_user.id == user_id:

            #BLINDAJE: Fuerzo que el ID del objeto sea SIEMPRE el de la URL.
            user.id = user_id

            # Lo actualizo - (Reemplazar y retornar)
            users[index] = user

            return UpdateUserResponse(
                message="Usuario actualizado exitosamente",
                user= user
            )
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Usuario con ID {user_id} no encontrado."
    )










