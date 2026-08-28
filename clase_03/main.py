# Instalar antes en terminal: pip install pydantic
# Instalar antes : pip install 'pydantic[email]'
from pydantic import BaseModel, ValidationError, EmailStr, Field, HttpUrl, SecretStr, field_validator

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    apellido: str = Field(min_length=4)
    website: HttpUrl
    edad: int = Field(gt=18, lt=30)  # gt = mayor que 18, lt = menor que 30
    password: SecretStr
    cuil: int

    # Usamos field_validator apuntando al campo 'cuil'
    @field_validator('cuil')
    @classmethod
    def cuil_validator(cls, v: int):
        # Convertimos a string para contar los dígitos fácilmente
        if len(str(v)) != 11:
            raise ValueError('El CUIL debe tener exactamente 11 dígitos')
        # Siempre debes retornar el valor si pasa la validación
        return v



# PRUEBA DE FUNCIONAMIENTO
try:
    user1 = User(
        id=123, 
        name="Facu", 
        email="facundojesus@hotmail.com", 
        apellido="Citera",
        website="https://www.promiedos.com.ar/", 
        edad=25, 
        password="mi_password_secreto", # Pasado como string
        cuil=20401587293
    )

    print("Nombre del usuario creado:", user1.name)

except ValidationError as ex:
    print("Error de validación:\n", ex)


