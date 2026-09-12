from models.User import CountryBase


class CountryResponse(CountryBase):
    id: int

class CreateCountryRequest(CountryBase):
    pass