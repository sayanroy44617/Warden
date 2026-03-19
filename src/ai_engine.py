import json
import uuid

from dotenv import load_dotenv
import os
import time
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
    def __init__(self, loki_url):
        self.loki_url = loki_url
        self.api_key = API_KEY
        self.client = httpx.AsyncClient()
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    async def analyze_incident(
        self, incident: Incident, logs: list[str]
    ) -> FixPlan | None:
        prompt = (
            f"You are a DevOps expert analyzing a container incident.\n\n"
            f"Container: {incident.container_name}\n"
            f"Anomaly: {incident.crash_reason}\n"
            f"Severity: {incident.severity.value}\n"
            f"Recent Logs:\n{chr(10).join(logs)}\n\n"
            f"Respond in this exact JSON format:\n"
            f"{{\n"
            f'  "root_cause": "...",\n'
            f'  "action": "restart" or "update_resources",\n'
            f'  "explanation": "plain english explanation",\n'
            f'  "parameters": {{}}\n'
            f"}}"
        )

        try:
            result = self.model.generate_content(prompt)
            text = result.text.strip()
            text = text.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(text)

            root_cause = parsed["root_cause"]
            action = parsed["action"]
            explanation = parsed["explanation"]
            parameters = parsed["parameters"]

            return FixPlan(
                id=uuid.uuid4().hex,
                incident_id=incident.id,
                action=action,
                explanation=explanation,
                parameters=parameters,
                root_cause=root_cause,
            )
        except json.JSONDecodeError as e:
            logger.error(f"Gemini returned invalid JSON: {e}")
            return None
        except KeyError as e:
            logger.error(f"Missing field in Gemini response: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error analyzing incident: {e}")
            return None

    async def get_logs_from_loki(self, container_name: str) -> list[str]:
        query = f'{{name="{container_name}"}}'
        params = {
            "query": query,
            "limit": 50,
            "start": int((time.time() - 600) * 1e9),
            "end": int(time.time() * 1e9),
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
