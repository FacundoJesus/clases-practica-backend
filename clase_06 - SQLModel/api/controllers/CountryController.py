from api.payload.countriesDTO import CreateCountryRequest, CreateCountryResponse, GetCountriesResponse, GetCountryByIdResponse, UpdateCountryRequest
from fastapi import APIRouter
from models.users import Country
from repositories.database import SessionDep
from services import CountryService as countryService
from collections.abc import Sequence
from typing import Annotated
from fastapi import APIRouter, HTTPException, Query

router = APIRouter()


# Crear País
@router.post("/country", response_model=CreateCountryResponse)
def createCountry(req: CreateCountryRequest, session: SessionDep) -> Country:
    return countryService.createCountry(session, req)


# Obtener todos los paises
@router.get("/country", response_model=Sequence[GetCountriesResponse])
def getCountries(session: SessionDep, offset: int = 0,limit: Annotated[int, Query(le=100)] = 100) -> Sequence[Country]:
    return countryService.getCountries(session, offset, limit)

# Obtener país por Id
@router.get("/country/{country_id}", response_model=GetCountryByIdResponse)
def getCountryById(country_id: int, session: SessionDep) -> Country:
    country = countryService.getCountryById(session, country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country does not exist")
        
    return country


# Buscar país por nombre
@router.get("/country/search/{name}")
def getCountryByName(name: str, session: SessionDep) -> Sequence[Country]:
    return countryService.getCountryByName(session, name)

# Eliminar país
@router.delete("/country/{country_id}")
def deleteCountryById(country_id: int, session: SessionDep):
    deleted = countryService.deleteCountryById(session, country_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Country not found")
    
    return {"message": f"Country {country_id} deleted successfully"}

# Actualizar país
@router.put("/country/{country_id}", response_model=GetCountryByIdResponse)
def updateCountry(country_id: int, req: UpdateCountryRequest, session: SessionDep) -> Country:
    country = countryService.updateCountry(session, country_id, req)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country
