
from Country import Country
from sqlmodel import Field, Relationship, SQLModel


# Nivel de negocio 
class UserBase(SQLModel):
    name: str = Field(index=True)
    age: int
    country_id: int | None = Field(default=None, foreign_key="country.id")
    password: str | None = Field(default=None)
    
#Nivel de DB
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    country: Country | None = Relationship(back_populates="users")


