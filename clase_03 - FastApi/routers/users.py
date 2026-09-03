# Para correr la FastApi: python -m uvicorn api:app --reload
from fastapi import APIRouter, HTTPException, status
from models.users import User, GetUsersResponse, CreateUserResponse, DeleteUserResponse, UpdateUserResponse

router = APIRouter()

# Array de usuarios
users = []

user1 = User(
    id=1,
    firstName="Juan",
    lastName="Perez",       
    email="juan.perez@example.com",
    age=25,                
    cuil=20384756291,       
    isActive=True
)
user2 = User(
    id=2,
    firstName="Maria",
    lastName="Gomez",       
    email="maria.gomez@example.com",
    age=21,                
    cuil=27493827164,       
    isActive=True
)
user3 = User(
    id=3,
    firstName="Lucas",
    lastName="Rodriguez",   
    email="lucas.rod@example.com",
    age=28,                
    cuil=20123456789,       
    isActive=False          
)
users.append(user1)
users.append(user2)
users.append(user3)


# Obtener todos los usuarios
@router.get("/users")
def get_all_users() -> GetUsersResponse:
    
    if not users:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Users not found"
        )
    
    return GetUsersResponse(users= users)


# Obtener Usuarios Activos
@router.get("/users/active")
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
@router.get("/users/inactive")
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
@router.post("/users")
def create_user(user: User) -> CreateUserResponse:

    for existUser in users:
        if existUser.id == user.id:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= f"User with ID {user.id} already exists"
            )
        
    users.append(user)

    return CreateUserResponse(
        message="User created successfully",
        user= user
    )


# Eliminar Usuario
@router.delete("/users/{id}")
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


# Actualizar Usuario existente
@router.put("/users/{id}")
def update_user(id: int, user:User) -> UpdateUserResponse:

    for index, existing_user in enumerate(users):
        if existing_user.id == id:

            #BLINDAJE: Fuerzo que el ID del objeto sea SIEMPRE el de la URL.
            user.id = id

            # Lo actualizo - (Reemplazar y retornar)
            users[index] = user

            return UpdateUserResponse(
                message="User updated successfully",
                user= user
            )
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with ID {id} not found"
    )