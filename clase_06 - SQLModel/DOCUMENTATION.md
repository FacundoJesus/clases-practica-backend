# Documentación del Proyecto FastAPI & SQLModel

Este proyecto es una API RESTful desarrollada con **FastAPI** y **SQLModel**, diseñada para gestionar usuarios y países. Utiliza **SQLite** como base de datos local y sigue un patrón de arquitectura en capas bien definido.

## Tecnologías Utilizadas

* **FastAPI**: Framework web de alto rendimiento para construir APIs en Python.
* **SQLModel**: ORM (Object-Relational Mapping) que combina la potencia de SQLAlchemy y la validación de Pydantic, diseñado específicamente para trabajar con FastAPI.
* **SQLite**: Motor de base de datos relacional ligero utilizado para el almacenamiento de datos (`database.db`).
* **Uvicorn**: Servidor ASGI utilizado para ejecutar la aplicación.

## Estructura del Proyecto

El proyecto está organizado bajo un patrón de capas para separar responsabilidades (MVC / N-Capas):

```text
.
├── main.py                  # Punto de entrada de la aplicación
├── database.db              # Base de datos SQLite (se genera automáticamente)
├── README.md                # Instrucciones de instalación
├── api/                     # Capa de presentación y contratos
│   ├── controllers/         # Enrutadores (Routers) de FastAPI (endpoints)
│   │   ├── CountryController.py
│   │   └── UserController.py
│   └── payload/             # DTOs (Data Transfer Objects) y Schemas (Pydantic/SQLModel)
│       ├── countriesDTO.py
│       └── usersDTO.py
├── models/                  # Capa de Datos / Entidades de Base de Datos
│   └── users.py             # Definición de tablas `User` y `Country`
├── repositories/            # Capa de Acceso a Datos (Infraestructura)
│   └── database.py          # Configuración del Engine de SQLModel y dependencias de sesión
└── services/                # Capa de Lógica de Negocio
    ├── CountryService.py
    └── UserService.py
```

### Descripción de las Capas

1. **`main.py`**: Configura la instancia de FastAPI, registra los routers (controladores) y maneja eventos del ciclo de vida de la app, como la creación de la base de datos y la inyección de datos de prueba (`create_dummy_data`) al iniciar.
2. **`models/`**: Define la estructura de las tablas en la base de datos utilizando SQLModel. Aquí encontramos las entidades `User` y `Country` y sus relaciones.
3. **`api/payload/ (DTOs)`**: Define los esquemas (modelos de Pydantic) utilizados para validar las peticiones entrantes (Requests) y dar formato a las respuestas salientes (Responses). Evita exponer directamente los modelos de base de datos.
4. **`api/controllers/`**: Define los *endpoints* de la API (rutas HTTP). Se encarga de recibir la petición HTTP, llamar al servicio correspondiente (inyectándolo como dependencia) y retornar la respuesta al cliente. Ya no conoce detalles de infraestructura como sesiones de base de datos.
5. **`services/`**: Contiene la lógica de negocio encapsulada en Clases. Recibe instrucciones desde los controladores, procesa reglas e interactúa con la base de datos. La sesión de la base de datos se inyecta directamente en su constructor.
6. **`repositories/`**: Centraliza la conexión con la base de datos. Define el `engine` de conexión y proporciona la dependencia `SessionDep` para inyectar la sesión de la base de datos en los servicios.

---

## Endpoints Disponibles

La aplicación cuenta con documentación interactiva provista automáticamente por FastAPI (Swagger UI). Una vez iniciada la app, puedes acceder a ella en: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### Usuarios (`/user`)

* `GET /user`: Obtiene una lista paginada de todos los usuarios.
* `GET /user/{user_id}`: Obtiene el detalle de un usuario específico por su ID (incluyendo su país asociado).
* `GET /user/search/{name}`: Busca usuarios por coincidencia en el nombre.
* `GET /user_mayores`: Obtiene la lista de usuarios que son mayores de edad (edad >= 18).
* `POST /user`: Crea un nuevo usuario.
* `PUT /user/{user_id}`: Actualiza la información de un usuario existente.
* `DELETE /user/{user_id}`: Elimina un usuario por su ID.

### Países (`/country`)

* `GET /country`: Obtiene una lista paginada de todos los países.
* `GET /country/{country_id}`: Obtiene el detalle de un país específico por su ID.
* `GET /country/search/{name}`: Busca países por coincidencia en el nombre.
* `POST /country`: Crea un nuevo país.
* `PUT /country/{country_id}`: Actualiza la información de un país existente.
* `DELETE /country/{country_id}`: Elimina un país por su ID.

## Ejecución del Proyecto

Para ejecutar la aplicación localmente, asegúrate de tener tu entorno virtual activado y ejecuta:

```bash
uvicorn main:app --reload
```
