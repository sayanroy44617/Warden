import docker
import asyncio
from src.models.fixplan import FixPlan, FixActionEnum
from src.models.fixresult import FixResult


class FixExecutor:
    def __init__(self):
        self.client = docker.from_env()

    async def execute_fix(self, fix_plan: FixPlan) -> FixResult:
        action_map = {
            FixActionEnum.RESTART: self._restart_container,
            FixActionEnum.UPDATE_RESOURCES: self._update_resources,
            FixActionEnum.EXEC_COMMAND: self._exec_command,
        }

        handler = action_map.get(fix_plan.action)

        if handler is None:
            raise ValueError(f"Invalid action: {fix_plan.action}")

        await handler(fix_plan)
        return FixResult(success=True)

    async def _restart_container(self, fix_plan: FixPlan):
        container = self.client.containers.get(fix_plan.container_name)
        await asyncio.to_thread(container.restart)

    async def _update_resources(self, fix_plan: FixPlan):
        container = self.client.containers.get(fix_plan.container_name)
        await asyncio.to_thread(
            container.update,
            mem_limit=fix_plan.parameters.get("memory"),
            cpu_quota=fix_plan.parameters.get("cpu"),
        )

    async def _exec_command(self, fix_plan: FixPlan):
        container = self.client.containers.get(fix_plan.container_name)
        await asyncio.to_thread(container.exec_run, fix_plan.parameters.get("command"))
