---
trigger: always_on
---

# Reglas de Arquitectura en Capas

1. **`main.py`**: Configura la instancia de FastAPI, registra los routers (controladores) y maneja eventos del ciclo de vida de la app, como la creación de la base de datos y la inyección de datos de prueba (`create_dummy_data`) al iniciar.
2. **`models/`**: Define la estructura de las tablas en la base de datos utilizando SQLModel. Aquí encontramos las entidades `User` y `Country` y sus relaciones.
3. **`api/payload/ (DTOs)`**: Define los esquemas (modelos de Pydantic) utilizados para validar las peticiones entrantes (Requests) y dar formato a las respuestas salientes (Responses). Evita exponer directamente los modelos de base de datos.
4. **`api/controllers/`**: Define los *endpoints* de la API (rutas HTTP). Se encarga de recibir la petición HTTP, llamar al servicio correspondiente y retornar la respuesta al cliente.
5. **`services/`**: Contiene la lógica de negocio. Recibe instrucciones desde los controladores, procesa reglas si las hay, e interactúa con la base de datos para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar).
6. **`repositories/`**: Centraliza la conexión con la base de datos. Define el `engine` de conexión y proporciona la dependencia `SessionDep` para inyectar la sesión de la base de datos en los controladores.

. Cada folder/carpeta que creado debe tener un archivo llamado __init__.py