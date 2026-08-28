# Instalar antes: pip install FastApi
# Para correr la FastApi: python -m uvicorn api:app --reload

from fastapi import FastAPI
from main import User

app = FastAPI()

@app.get("/")
def get():
    return {"mensaje": "Hola Mundo!"}

@app.post("/usuarios/")
def crearUsuario(usuario: User):
    # FastAPI ya validó automáticamente que los datos cumplan con el modelo 'User'
    
    # Aquí simularías guardar los datos en una base de datos.
    # Por ahora, simplemente devolvemos un mensaje de éxito con los datos recibidos.
    return {
        "mensaje": "Usuario creado con éxito",
        "usuario_recibido": usuario
    }


