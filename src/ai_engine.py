from dotenv import load_dotenv
import os , time
import httpx
import logging

from src.models.fixplan import FixPlan
from src.models.incident import Incident
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AIEngine:

    def __init__(self , loki_url ):
        self.loki_url = loki_url
        self.api_key = API_KEY
        self.client = httpx.AsyncClient()
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    async def analyze_incident(self , incident : Incident) -> FixPlan:
        pass

    async def get_logs_from_loki(self , container_name : str) -> list[str]:
        query = f'{{name="{container_name}"}}'
        params = {
            "query": query,
            "limit" : 50 ,
            "start" : int((time.time() - 600) * 1e9),
            "end" : int(time.time() * 1e9)
        }
        loki_log_url = f"{self.loki_url}/loki/api/v1/query_range"

        try:
            response = await self.client.get(loki_log_url, params=params)
            logs = []
            for stream in response.json()["data"]["result"]:
                for value in stream["values"]:
                    logs.append(value[1])
            return logs
        except httpx.TimeoutException:
            logger.error("Timeout fetching Loki logs")
            return []
        except httpx.HTTPStatusError as e:
            logger.error(f"Error fetching Loki logs: {e.response.text}")
            return []
        except httpx.RequestError as e:
            logger.error(f"Error fetching Loki logs: {e}")
            return []
        except Exception as e:
            logger.error(f"Error fetching Loki logs: {e}")
            return []


