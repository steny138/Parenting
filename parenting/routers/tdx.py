import logging
from fastapi import APIRouter
from pydantic import BaseModel
from ..services.tdx import TDX

import os
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

# initial itofoo service
services = TDX(os.getenv("TDXApiId"),
               os.getenv("TDXApiKey"))

router = APIRouter(
    prefix="/tdx",
    tags=["tdx", "bus", "traffic"],
)


class Response(BaseModel):
    code: str
    response: object

# Route id 131577


@router.get("/test", response_model=Response)
async def test():
    estimate = services.get_bus_estimate_time("NewTaipei", "704", 131511)

    return {"code": (200 if estimate else 404), "response": estimate}
