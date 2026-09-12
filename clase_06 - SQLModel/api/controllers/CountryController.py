from api.payload.countries import CreateCountryRequest, CreateCountryResponse
from fastapi import APIRouter
from models.users import Country
from repositories.database import SessionDep
from services import CountryService as countryService

router = APIRouter()


# Crear País
@router.post("/country", response_model=CreateCountryResponse)
def createCountry(req: CreateCountryRequest, session: SessionDep) -> Country:
    return countryService.createCountry(session, req)
