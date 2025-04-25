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


@router.put("/logout/forced", dependencies=[Depends(AuthGaurd)], name="forced_logout")
async def logout_forced(
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

@router.post("/forgot-password")
async def forgot_password(
    payload: ForgotPasswordRequest,
    request: Request
):
    return await AuthController().forgot_password(payload, request)


@router.post("/change-password", dependencies=[Depends(AuthGaurd)])
async def change_password(
    payload: ChangePasswordRequest,
    request: Request,
    auth: AuthGaurd = Depends(AuthGaurd)
):
    access_token: str = auth.valid_token()
    return await AuthController().change_password(payload, request)