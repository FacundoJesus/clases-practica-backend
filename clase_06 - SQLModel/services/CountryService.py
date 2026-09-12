from api.payload.countries import CreateCountryRequest
from models.users import Country
from sqlmodel import Session


def createCountry(session: Session, req: CreateCountryRequest) -> Country:
    country = Country(name=req.name)
    session.add(country)
    session.commit()
    session.refresh(country)
    return country
