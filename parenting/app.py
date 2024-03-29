import logging
import random
import string
import time
from fastapi import FastAPI
from starlette.requests import Request

from .routers import parenting, tdx

app = FastAPI(debug=True)

app.include_router(parenting.router)
app.include_router(tdx.router)

logger = logging.getLogger(__name__)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)

    logger.info(f"rid={idem}" +
                f" completed_in={formatted_process_time}ms" +
                f" status_code={response.status_code}")

    response.headers["X-Process-Time"] = str(process_time)

    return response


@app.get("/")
def read_root():
    return {"Hello": "World"}
