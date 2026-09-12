#from collections.abc import Sequence
#from typing import Annotated


from api.payload.countries import CreateCountryRequest, CreateCountryResponse
from fastapi import APIRouter, HTTPException, Query
from models.users import Country
from repositories.database import SessionDep
from services import CountryService as countryService

router = APIRouter()

# Crear País
@router.post("/country", response_model=CreateCountryResponse)
def createCountry(countryRequest:CreateCountryRequest,session:SessionDep) -> Country:
    return countryService.createCountry(countryRequest,session)
