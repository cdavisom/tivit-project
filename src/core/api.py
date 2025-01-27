from fastapi import FastAPI

from src.core.routes import fake
from src.auth.routes import auth

app = FastAPI()

app.include_router(fake.router, prefix="/fake")
app.include_router(auth.router, prefix="/fake")
