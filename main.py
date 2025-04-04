from fastapi import FastAPI
from contextlib import asynccontextmanager

from routers import campaign_router
from db_setup import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run before the application starts
    init_db()
    print("Database tables created (if they didn't exist).")
    yield
    # Code to run when the application shuts down
    print("Application shutdown.")


app = FastAPI(lifespan=lifespan)
app.include_router(campaign_router)
