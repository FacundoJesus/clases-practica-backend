from sqlmodel import Field, SQLModel, create_engine

# Se define el modelo
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}";

connect_args = {"check_same_thread": False}  # Solo para SQLite
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)