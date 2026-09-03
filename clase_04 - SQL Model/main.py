from sqlmodel import Field, SQLModel

# Se define el modelo
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)


