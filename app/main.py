from fastapi import FastAPI
from app.api.v1.api import api_router
from app.config import settings
from app.database import engine
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get('/')
def root():
    return {"message": "Welcome to AncestraLink API"}

@app.on_event("startup")
def test_db_connection():
    try:
        with engine.connect() as connection:
            print("Database connection successful!")
    except OperationalError as e:
        print("Database connection failed:", e)
