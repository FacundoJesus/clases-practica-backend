from sqlmodel import Field, Relationship, SQLModel

# Nivel de negocio 
class Country(SQLModel):
    name: str = Field(index=True)

# Nivel de DB
class CountryDB(Country, table=True):
    id: int | None = Field(default=None, primary_key=True)
    users: list["UserDB"] = Relationship(back_populates="country")


# Nivel de negocio 
class User(SQLModel):
    name: str = Field(index=True)
    age: int
    country_id: int | None = Field(default=None, foreign_key="countrydb.id")
    password: str | None = Field(default=None)

# Nivel de DB ..
class UserDB(User, table=True):
    id: int | None = Field(default=None, primary_key=True)
    country: CountryDB | None = Relationship(back_populates="users")