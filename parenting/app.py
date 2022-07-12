from fastapi import FastAPI
from .routers import parenting

app = FastAPI(debug=True)

app.include_router(parenting.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
