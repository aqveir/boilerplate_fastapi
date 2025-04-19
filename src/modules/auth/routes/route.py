from typing import Any
from fastapi import APIRouter, Depends, Request

# Include the project controllers
from ..controllers.controller import AuthController

# Include the project models
from ..models.request import *

# Import middlewares and dependencies
from modules.base.fastapi.decorations.security import test_permissions
from modules.base.fastapi.dependencies.authentication import AuthGaurd

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
async def authenticate(
    credentials: LoginRequest, 
    request: Request
):
    return await AuthController().authenticate(credentials, request)


@router.put("/logout", dependencies=[Depends(AuthGaurd)])
async def logout(
    auth: AuthGaurd = Depends(AuthGaurd)
):
    access_token: str = auth.valid_token()
    return await AuthController().logout(access_token, is_forced=False)


@router.put("/logout/forced", dependencies=[Depends(AuthGaurd)])
async def logout(
    auth: AuthGaurd = Depends(AuthGaurd)
):
    access_token: str = auth.valid_token()
    return await AuthController().logout(access_token, is_forced=True)


@router.post("/register")
async def register(
    payload: RegisterRequest,
    request: Request
):
    return await AuthController().register(payload, request)