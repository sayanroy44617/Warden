import asyncio
import logging
import uuid
from datetime import datetime

import httpx
from .models.incident import Incident, SeverityEnum, IncidentStatusEnum

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Monitor:
    """
    Monitors system health using Prometheus metrics.

    Attributes:
        client: HTTP client for making requests to Prometheus
        prometheus_url: Base URL of the Prometheus server
    """

    def __init__(self, prometheus_url):
        self.client = httpx.AsyncClient()
        self.prometheus_url = prometheus_url

    async def get_prometheus_data(self, promql: str):
        """
        Fetches Prometheus metrics data.

        Returns:
            dict: Prometheus metrics data
        """
        try:
            prometheus_query_url = f"{self.prometheus_url}/api/v1/query"
            params = {"query": promql}

            response = await self.client.get(
                prometheus_query_url, params=params, timeout=5
            )
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            logger.error("Timeout fetching Prometheus data")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"Error fetching Prometheus data: {e.response.text}")
            return None
        except httpx.RequestError as e:
            logger.error(f"Error fetching Prometheus data: {e}")
            return None
        except Exception as e:
            logger.error(f"Error fetching Prometheus data: {e}")
            return None

    async def start_monitoring(self):
        while True:
            await self.check_cpu()
            await self.check_memory()
            await self.check_restart_count()
            await asyncio.sleep(30)

    async def check_cpu(self):
        promql = 'rate(container_cpu_usage_seconds_total{image!=""}[1m]) * 100'
        data = await self.get_prometheus_data(promql)
        if data is None:
            return None
        for result in data["data"]["result"]:
            container_name = result["metric"]["name"]
            cpu_value = float(result["value"][1])
            logger.info(f"CPU usage for container {container_name}: {cpu_value}%")
            if cpu_value > 80:
                incident = Incident(
                    id=uuid.uuid4().hex,
                    timestamp=datetime.now(),
                    container_name=container_name,
                    logs=[],
                    crash_reason="HIGH CPU USAGE",
                    severity=SeverityEnum.HIGH,
                    incident_status=IncidentStatusEnum.DETECTED,
                )
                logger.warning(f"Incident created for {container_name}: HIGH CPU")
                return incident
        return None

    async def check_memory(self):
        promql = 'container_memory_usage_bytes{image!=""} / container_spec_memory_limit_bytes{image!=""} * 100'
        data = await self.get_prometheus_data(promql)
        if data is None:
            return None
        for result in data["data"]["result"]:
            container_name = result["metric"]["name"]
            memory_value = float(result["value"][1])
            logger.info(f"Memory usage for container {container_name}: {memory_value}%")
            if memory_value > 85:
                incident = Incident(
                    id=uuid.uuid4().hex,
                    timestamp=datetime.now(),
                    container_name=container_name,
                    logs=[],
                    crash_reason="HIGH MEMORY USAGE",
                    severity=SeverityEnum.HIGH,
                    incident_status=IncidentStatusEnum.DETECTED,
                )
                logger.warning(f"Incident created for {container_name}: HIGH MEMORY")
                return incident
        return None

    async def check_restart_count(self):
        promql = 'container_restart_count{image!=""}'
        data = await self.get_prometheus_data(promql)
        if data is None:
            return None
        for result in data["data"]["result"]:
            container_name = result["metric"]["name"]
            restart_count = int(result["value"][1])
            logger.info(f"Restart for container {container_name}: {restart_count}%")
            if restart_count > 3:
                incident = Incident(
                    id=uuid.uuid4().hex,
                    timestamp=datetime.now(),
                    container_name=container_name,
                    logs=[],
                    crash_reason="HIGH RESTART COUNT",
                    severity=SeverityEnum.CRITICAL,
                    incident_status=IncidentStatusEnum.DETECTED,
                )
                logger.warning(f"Incident created for {container_name}: Restart Count")
                return incident
