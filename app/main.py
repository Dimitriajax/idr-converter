from fastapi import FastAPI, Depends
from app.auth import validate_api_key
from .routers import convert

app = FastAPI(dependencies=[Depends(validate_api_key)])

app.include_router(convert.router)