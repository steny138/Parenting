import logging
from fastapi import APIRouter
from pydantic import BaseModel
from ..services.itofoo import Itofoo


logger = logging.getLogger("fastapi")

# initial itofoo service
services = Itofoo()

router = APIRouter(
    prefix="/parenting",
    tags=["parenting"],
)


class Response(BaseModel):
    code: str
    response: str


@router.get('/user')
async def get_user():
    return services.user_info()


@router.get("/baby")
async def get_baby():
    return services.baby_info()


@router.post("/baby/departure", response_model=Response)
async def departure():
    return services.baby_departured()


@router.post("/baby/arrivals", response_model=Response)
async def arrivals():
    return services.baby_arrivals()


@router.post("/baby/pickup", response_model=Response)
async def pickup():
    return services.pickup_baby()
