import logging
from fastapi import APIRouter
from pydantic import BaseModel
from ..services.itofoo import Itofoo

import os
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

# initial itofoo service
services = Itofoo(os.getenv("IToFooUserName"),
                  os.getenv("IToFooPassword"))
router = APIRouter(
    prefix="/parenting",
    tags=["parenting"],
)


class Response(BaseModel):
    code: str
    response: str


@router.get('/user_name')
async def get_user_name():
    return services.user_name


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
    services.set_ready_to_pickup()

    return services.baby_departure()

@router.post("/baby/arrivals", response_model=Response)
async def arrivals():
    return services.baby_arrivals()


@router.post("/baby/pickup", response_model=Response)
async def pickup():
    # if not services.could_pickup():
    #     return {}

    return services.pickup_baby()
