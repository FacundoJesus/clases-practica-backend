from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from api.payload.loginDTO import LoginRequest, LoginResponse
from services.LoginService import LoginService

router = APIRouter(tags=["Auth"])
LoginServiceDep = Annotated[LoginService, Depends(LoginService)]


@router.post("/login", response_model=LoginResponse)
def login(Loginreq: LoginRequest, service: LoginServiceDep) -> LoginResponse:
    valid = service.login(Loginreq.email, Loginreq.password)
    if not valid:
        raise HTTPException(status_code=401, detail="User/password incorrect")
    return LoginResponse(msg="ok", token="121456")