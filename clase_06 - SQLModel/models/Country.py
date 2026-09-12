from sqlmodel import Field, Relationship, SQLModel
from User import User


# Nivel de negocio
class CountryBase(SQLModel):
    name: str = Field(index=True)

#Nivel de DB
class Country(CountryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    users: list["User"] = Relationship(back_populates="country")

