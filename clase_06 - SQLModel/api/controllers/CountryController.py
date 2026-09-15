from api.payload.countriesDTO import CreateCountryRequest, CreateCountryResponse, GetCountriesResponse, GetCountryByIdResponse, UpdateCountryRequest
from fastapi import APIRouter, HTTPException, Query, Depends
from models.users import Country
from services.CountryService import CountryService
from collections.abc import Sequence
from typing import Annotated

router = APIRouter()


# Crear País
@router.post("/country", response_model=CreateCountryResponse)
def createCountry(req: CreateCountryRequest, service: CountryService = Depends()) -> Country:
    return service.createCountry(req)


# Obtener todos los paises
@router.get("/country", response_model=Sequence[GetCountriesResponse])
def getCountries(offset: int = 0, limit: Annotated[int, Query(le=100)] = 100, service: CountryService = Depends()) -> Sequence[Country]:
    return service.getCountries(offset, limit)

# Obtener país por Id
@router.get("/country/{country_id}", response_model=GetCountryByIdResponse)
def getCountryById(country_id: int, service: CountryService = Depends()) -> Country:
    country = service.getCountryById(country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country does not exist")
        
    return country


# Buscar país por nombre
@router.get("/country/search/{name}")
def getCountryByName(name: str, service: CountryService = Depends()) -> Sequence[Country]:
    return service.getCountryByName(name)

# Eliminar país
@router.delete("/country/{country_id}")
def deleteCountryById(country_id: int, service: CountryService = Depends()):
    deleted = service.deleteCountryById(country_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Country not found")
    
    return {"message": f"Country {country_id} deleted successfully"}

# Actualizar país
@router.put("/country/{country_id}", response_model=GetCountryByIdResponse)
def updateCountry(country_id: int, req: UpdateCountryRequest, service: CountryService = Depends()) -> Country:
    country = service.updateCountry(country_id, req)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country
