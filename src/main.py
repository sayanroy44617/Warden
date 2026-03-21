import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.approval_server import warden_router

logger = logging.getLogger("uvicorn")


app = FastAPI(title="Warden API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(warden_router)
