from fastapi import APIRouter, Depends
from modules.user.controllers.controller import UserController

# Import middlewares
from modules.base.fastapi.dependencies.authentication import AuthGaurd

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", dependencies=[Depends(AuthGaurd)])
async def index():
    return await UserController().index()

@router.get("/{hash}")
async def show(hash: str):
    return await UserController().show(hash)

@router.post("/")
async def create():
    return await UserController().create()

@router.put("/{hash}")
async def update(hash: str):
    return await UserController().update(hash)

@router.delete("/{hash}", dependencies=[Depends(AuthGaurd)])
async def delete(hash: str):
    return await UserController().delete(hash)
