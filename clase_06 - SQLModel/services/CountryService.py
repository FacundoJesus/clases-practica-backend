from api.payload.countriesDTO import CreateCountryRequest, UpdateCountryRequest
from models.users import Country
from sqlmodel import Session
from collections.abc import Sequence
from sqlmodel import Session, col, select
from typing import Optional


def createCountry(session: Session, req: CreateCountryRequest) -> Country:
    country = Country(name=req.name)
    session.add(country)
    session.commit()
    session.refresh(country)
    return country


def getCountries(session: Session, offset: int, limit: int) -> Sequence[Country]:
    statement = select(Country).offset(offset).limit(limit)
    return session.exec(statement).all()


def getCountryById(session: Session, countryId: int) -> Optional[Country]:
    return session.get(Country, countryId)


def getCountryByName(session: Session, name: str) -> Sequence[Country]:
    statement = select(Country).where(col(Country.name).like(f"%{name}%"))
    return session.exec(statement).all()


def deleteCountryById(session: Session, country_id: int) -> bool:
    country = session.get(Country, country_id)
    if not country:
        return False
    
    session.delete(country)
    session.commit()
    return True


def updateCountry(session: Session, country_id: int, req: UpdateCountryRequest) -> Optional[Country]:
    country = session.get(Country, country_id)
    if not country:
        return None
    
    if req.name is not None:
        country.name = req.name

    session.add(country)
    session.commit()
    session.refresh(country)
    return country