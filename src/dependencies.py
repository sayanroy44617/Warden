import os

from dotenv import load_dotenv

from src.ai_engine import AIEngine
from src.fix_executor import FixExecutor
from src.monitor import Monitor
from src.notifier import Notifier

load_dotenv()

monitor = Monitor(os.getenv("PROMETHEUS_URL"))
ai_engine = AIEngine(loki_url=os.getenv("LOKI_URL"))
notifier = Notifier()
fix_executor = FixExecutor()
