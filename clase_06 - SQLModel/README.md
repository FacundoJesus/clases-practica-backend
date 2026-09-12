# 1. Crear entorno virtual
python -m venv venv

# 2. Activar el entorno virtual
venv\Scripts\activate

# 3. Instalar dependencias
pip install fastapi sqlmodel uvicorn

# 4. Para hacerlo correr
fastapi dev main.py
uvicorn main:app --reload