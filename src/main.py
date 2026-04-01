import asyncio
import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dependencies import monitor, ai_engine, notifier
from approval_server import warden_router
from redis_client import get_redis_client

logger = logging.getLogger("uvicorn")
redis = get_redis_client()


async def monitoring_loop():
    while True:
        incidents = await monitor.check_all()
        for incident in incidents:
            logs = await ai_engine.get_logs_from_loki(incident.container_name)
            fix_plan = await ai_engine.analyze_incident(incident, logs)
            if fix_plan:
                await redis.set(f"fixplan:{fix_plan.id}", fix_plan.model_dump_json())
                await notifier.send_alert_email(incident, fix_plan)
        await asyncio.sleep(30)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Warden API")
    asyncio.create_task(monitoring_loop())
    yield
    # shutdown — runs when app stops
    await monitor.client.aclose()


app = FastAPI(title="Warden API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(warden_router)
