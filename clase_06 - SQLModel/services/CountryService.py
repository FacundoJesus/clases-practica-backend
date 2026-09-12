from api.payload.countries import CreateCountryRequest
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