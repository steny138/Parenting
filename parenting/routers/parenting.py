import logging
from fastapi import APIRouter
from pydantic import BaseModel
from ..services.itofoo import Itofoo
from ..services.tdx import TDX

import os
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

# initial itofoo service
services = Itofoo(os.getenv("IToFooUserName"),
                  os.getenv("IToFooPassword"))

tdx = TDX(os.getenv("TDXApiId"),
          os.getenv("TDXApiKey"))

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

    #estimates = []
    #estimates.append(tdx.get_bus_estimate_time("NewTaipei", "704", 131511))

    #services.set_ready_to_pickup()

    resp = services.baby_departure()

    #resp["estimate"] = estimates

    return resp


@router.post("/baby/arrivals", response_model=Response)
async def arrivals():
    return services.baby_arrivals()


@router.post("/baby/test_pickup", response_model=Response)
async def test_pickup():
    services.set_ready_to_pickup()

    return {
        "code": "OK",
        "response": "right now"
    }


@ router.post("/baby/pickup", response_model=Response)
async def pickup():
    if not services.could_pickup():
        return {}

    return services.pickup_baby()
