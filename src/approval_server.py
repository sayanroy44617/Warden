import json
import logging

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from src.fix_executor import FixExecutor
from src.models.fixplan import FixPlan
from src.redis_client import get_redis_client
from src.dependencies import fix_executor

warden_router = APIRouter()
redis = get_redis_client()

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)


@warden_router.get("/approve/{incident_id}")
async def approve_incident(incident_id: str, executor :FixExecutor = Depends(lambda: fix_executor)):
    fix_plan = await redis.get(f"fixplan:{incident_id}")

    if fix_plan is None:
        raise HTTPException(status_code=404, detail="Fixplan not found")

    parsed = FixPlan(**json.loads(fix_plan))
    logger.info(f"Fixplan approved: {parsed}")
    execution_response =  await executor.execute_fix(parsed)
    await redis.delete(f"fixplan:{incident_id}")
    return {"message": "Fixplan approved", "execution_response": execution_response}



@warden_router.get("/reject/{incident_id}")
async def deny_incident(incident_id: str):
    if not await redis.exists(f"fixplan:{incident_id}"):
        raise HTTPException(status_code=404, detail="Fixplan not found")

    await redis.delete(f"fixplan:{incident_id}")
    return {"message": "Fixplan rejected"}


@warden_router.get("/incidents")
async def all_incident():
    return {"incidents": []}
