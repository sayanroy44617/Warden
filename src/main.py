import asyncio
import logging

from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.dependencies import monitor
from src.approval_server import warden_router
from src.monitor import Monitor

logger = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(app: FastAPI ):
    logger.info("Starting Warden API")
    asyncio.create_task(monitor.start_monitoring())
    yield
    # shutdown — runs when app stops
    await monitor.client.aclose()

app = FastAPI(title="Warden API" , lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(warden_router)
