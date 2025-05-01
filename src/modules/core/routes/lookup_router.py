""" Import the required modules """
from typing import Any
from fastapi import APIRouter, Depends, Request

# Import middlewares and dependencies
from modules.base.fastapi.dependencies.authentication import AuthGaurd

# Include the project controllers
from ..controllers.lookup_controller import LookupController as Controller

# Include the project models
from ..models.organization.request import (
    OrganizationCreateRequest,
    OrganizationUpdateRequest
)

# Create the module router
router = APIRouter(prefix="/lookup", tags=["LookUp"])


@router.get("/",
        dependencies=[Depends(AuthGaurd)],
        name="get_lookups"
    )
async def index(
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Get all model data.
    """
    current_user = auth.current_user()
    return await Controller().index(request, current_user)


@router.get("/{uid}",
        dependencies=[Depends(AuthGaurd)],
        name="get_lookup"
    )
async def show(
        uid: str,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Get the data with the given uid.
    """
    current_user = auth.current_user()
    return await Controller().show(uid, request, current_user)


@router.post("/",
        dependencies=[Depends(AuthGaurd)],
        name="create_lookup"
    )
async def create(
        payload: OrganizationCreateRequest,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Create a new model with the given payload.
    """
    current_user = auth.current_user()
    return await Controller().create(
            payload, request,
            current_user
        )


@router.put("/{uid}",
        dependencies=[Depends(AuthGaurd)],
        name="update_lookup"
    )
async def update(
        uid: str,
        payload: OrganizationUpdateRequest,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Update the model with the given uid and payload.
    """
    current_user = auth.current_user()
    return await Controller().update(
        uid, payload, request,
        current_user
    )


@router.delete("/{uid}",
        dependencies=[Depends(AuthGaurd)],
        name="delete_lookup"
    )
async def delete(
        uid: str,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Delete the model with the given uid and payload.
    """
    current_user = auth.current_user()
    return await Controller().delete(
        uid, request,
        current_user
    )
