# Proyecto Backend con FastAPI y SQLModel - Constitución y Reglas

Este archivo define la constitución del proyecto, el estilo de código para SQLModel, las restricciones arquitectónicas y los flujos permitidos para mantener una base de código limpia y modular. Los agentes y desarrolladores que trabajen en este proyecto deben seguir estrictamente estas directrices.

## 1. Constitución del Proyecto

El proyecto es un backend construido utilizando **FastAPI** como framework web y **SQLModel** como ORM (Object-Relational Mapping). La estructura de directorios sigue una arquitectura de capas separando responsabilidades:

- **`api/controllers/`**: Define los enrutadores de FastAPI (endpoints). Maneja las solicitudes HTTP, delega la lógica de negocio a los servicios y retorna las respuestas (formateadas utilizando DTOs).
- **`api/payload/`**: Contiene los Data Transfer Objects (DTOs), como esquemas de Pydantic, que se utilizan para validar los payloads de entrada y dar forma a las respuestas de salida (ej. `CreateUserRequest`, `GetUserWithCountryResponse`).
- **`api/middlewares/`**: Interceptores globales o específicos para procesar las peticiones HTTP antes de que lleguen a los controladores (ej. chequeo de API keys, contadores de uso).
- **`services/`**: Contiene la lógica de negocio del dominio. Define interfaces abstractas y clases concretas. Los servicios orquestan las operaciones y dependen de los repositorios para la persistencia.
- **`repositories/`**: Capa de persistencia. Contiene toda la lógica que interactúa con la base de datos a través de las sesiones de SQLModel (ejecución de consultas, inserciones, actualizaciones y borrados).
- **`models/`**: Define las entidades del sistema utilizando SQLModel. Separa claramente los modelos de negocio y los modelos específicos de base de datos (con tablas y relaciones).

## 2. Estilo de Código para SQLModel

El patrón para utilizar SQLModel en este proyecto implica separar los modelos de negocio puro de los modelos de base de datos para evitar acoplamiento y asegurar la integridad de la herencia:

- **Nivel de Negocio**: 
  Se define la clase base heredando directamente de `SQLModel`. Contiene únicamente los atributos que son campos lógicos de los datos.
  ```python
  class User(SQLModel):
      name: str = Field(index=True)
      age: int
      country_id: int | None = Field(default=None, foreign_key="countrydb.id")
      # ...otros atributos
  ```

- **Nivel de Base de Datos**:
  Se define la clase heredando del modelo de negocio, añadiendo `table=True`, la clave primaria y definiendo las relaciones de base de datos mediante `Relationship`.
  ```python
  class UserDB(User, table=True):
      id: int | None = Field(default=None, primary_key=True)
      country: CountryDB | None = Relationship(back_populates="users")
  ```

- Las consultas en los repositorios deben utilizar la sintaxis declarativa y tipada de `sqlmodel`, usando métodos como `select`, `col` y el objeto `Session` (`self.session.exec(statement)`).

## 3. Restricciones Arquitectónicas y Flujos Permitidos

El sistema utiliza la **Inyección de Dependencias** fuertemente (mediante `fastapi.Depends` y `Annotated`) para conectar las distintas capas. Se debe cumplir estrictamente el siguiente flujo:

### Flujo de Datos Permitido:
**Solicitud HTTP -> Controlador -> Servicio -> Repositorio -> Base de Datos -> Repositorio -> Servicio -> Controlador -> Respuesta HTTP**

### Reglas Estrictas:
1. **Los Controladores NUNCA interactúan con la Base de Datos:**
   Un controlador no puede inyectar ni recibir un objeto `Session`. Solamente debe inyectar abstracciones de la capa de Servicios (ej. `UserServiceInterface`).
2. **Los Controladores son responsables del Mapeo:**
   Los controladores reciben DTOs de `api/payload`, extraen la información y deben instanciar objetos del "Nivel de Negocio" (ej. `User`) antes de pasarlos a los servicios.
3. **Los Servicios NUNCA manejan primitivas HTTP:**
   Un servicio no debe recibir ni retornar objetos tipo `Request`, `Response` o lanzar excepciones HTTP (como `HTTPException`). Si ocurre un error de negocio, deben retornar `None` o lanzar excepciones de dominio que el controlador capturará e interpretará.
4. **Los Servicios dependen de Interfaces:**
   La capa de servicios debe definir interfaces (`UserServiceInterface`) y la implementación concreta (`UserService`) recibe la inyección del repositorio a través de anotaciones (`UserRepositoryDep = Annotated[UserRepository, Depends(UserRepository)]`).
5. **Los Repositorios centralizan las transacciones:**
   Toda manipulación de la BD ocurre aquí (`add`, `commit`, `refresh`, `delete`). Reciben los modelos de negocio y construyen los modelos de base de datos (`UserDB`).
6. **Las Respuestas en el Controlador:**
   El Controlador debe definir el formato de salida mediante el argumento `response_model` del decorador del router (ej. `@router.get("/user", response_model=Sequence[GetUsersResponse])`), y confiar en que FastAPI serializará correctamente el objeto (generalmente de tipo `ModelDB`) retornado por el servicio.


## 4. Autenticación, Autorización y Middlewares

- **Middlewares (`api/middlewares/`)**:
  - Deben ser clases que encapsulan la lógica de intercepción (ej. `CheckApikeyMW`).
  - Interceptan las peticiones HTTP antes de que lleguen a los controladores.
  - Tienen la responsabilidad de autorizar o denegar el acceso devolviendo primitivas de respuesta directa (como `JSONResponse`) en caso de error, o de delegar el flujo a la siguiente capa utilizando `call_next(request)`.
- **Login y Seguridad (`services/`, `utils/`)**:
  - La validación de credenciales (correo y contraseña) se debe realizar en la capa de servicios (ej. `LoginService`), consultando al repositorio.
  - La creación y manejo de tokens (JWT) se aísla en servicios especializados (ej. `JWTService`).
  - El hashing y verificación de contraseñas no debe estar ni en el controlador ni en el servicio directamente; debe extraerse a utilidades genéricas en el directorio `utils/` (ej. `utils/hash.py`).
  - El controlador (`login_controller.py`) solo recibe el DTO, coordina los servicios de validación y de tokens, y retorna la respuesta final (`LoginResponse`), lanzando `HTTPException` únicamente si falla el proceso (siguiendo las excepciones de negocio delegadas al controlador).
