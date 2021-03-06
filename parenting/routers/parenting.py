import json
import logging
from fastapi import APIRouter
from pydantic import BaseModel
from ..services.itofoo import Itofoo
import uvicorn

logger = logging.getLogger(__name__)

# initial itofoo service
services = Itofoo()
uvicorn.Config
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


@router.get("/test", response_model=Response)
async def test():
    result = services.baby_info()
    resp = Response(**result)
    logger.info(resp)
    return result


@router.post("/baby/departure", response_model=Response)
async def departure():
    return services.baby_departured()


@router.post("/baby/arrivals", response_model=Response)
async def arrivals():
    return services.baby_arrivals()


@router.post("/baby/pickup", response_model=Response)
async def pickup():
    return services.pickup_baby()
