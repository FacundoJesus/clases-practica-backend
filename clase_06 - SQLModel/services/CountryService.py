from api.payload.countriesDTO import CreateCountryRequest, UpdateCountryRequest
from models.users import Country
from collections.abc import Sequence
from sqlmodel import col, select
from typing import Optional
from repositories.database import SessionDep

class CountryService:
    def __init__(self, session: SessionDep):
        self.session = session

    def createCountry(self, req: CreateCountryRequest) -> Country:
        country = Country(name=req.name)
        self.session.add(country)
        self.session.commit()
        self.session.refresh(country)
        return country

    def getCountries(self, offset: int, limit: int) -> Sequence[Country]:
        statement = select(Country).offset(offset).limit(limit)
        return self.session.exec(statement).all()

    def getCountryById(self, countryId: int) -> Optional[Country]:
        return self.session.get(Country, countryId)

    def getCountryByName(self, name: str) -> Sequence[Country]:
        statement = select(Country).where(col(Country.name).like(f"%{name}%"))
        return self.session.exec(statement).all()

    def deleteCountryById(self, country_id: int) -> bool:
        country = self.session.get(Country, country_id)
        if not country:
            return False
        
        self.session.delete(country)
        self.session.commit()
        return True

    def updateCountry(self, country_id: int, req: UpdateCountryRequest) -> Optional[Country]:
        country = self.session.get(Country, country_id)
        if not country:
            return None
        
        if req.name is not None:
            country.name = req.name

        self.session.add(country)
        self.session.commit()
        self.session.refresh(country)
        return country