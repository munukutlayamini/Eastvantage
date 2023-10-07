from fastapi import FastAPI
from routers.address import router_address
from db import models
from db.database import engine

app = FastAPI()

@app.get('/health')
def health():
    return True

app.include_router(router_address)
models.Base.metadata.create_all(engine)