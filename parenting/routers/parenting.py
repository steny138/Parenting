import logging
from fastapi import APIRouter
from ..services.itofoo import Itofoo

from fastapi.logger import logger as fastapi_logger

logger = logging.getLogger("fastapi")
services = Itofoo()

router = APIRouter(
    prefix="/parenting",
    tags=["parenting"],
)


@router.get('/user')
async def get_user():
    logger.warning("get user info")
    fastapi_logger.warning("get user info 2")
    return services.user_info()


@router.get("/baby")
async def get_baby():
    return services.baby_info()


@router.post("/baby/departure")
async def departure():
    return services.baby_departured()


@router.post("/baby/arrivals")
async def arrivals():
    return services.baby_arrivals()


@router.post("/baby/pickup")
async def pickup():
    return services.pickup_baby()
