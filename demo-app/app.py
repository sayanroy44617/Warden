import time
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
mode = os.getenv("MODE")

def normal_operation():
    while True:
        logger.info("Demo Api is up and running")
        time.sleep(2)

def cpu_spike():
    logger.warning("WARN: CPU spike triggered")
    while True:
        x = 99999 ** 99999  # useless heavy calculation

def memory_leak():
    leak = []
    while True:
        leak.append("x" * 1024)  # 1KB per iteration, grows faster
        logger.warning(f"WARN: Memory growing, size: {len(leak)} items")
        time.sleep(0.1)

def crash():
    raise Exception("Demo Api crashed")

if __name__ == "__main__":
    if mode == "cpu_spike":
        cpu_spike()
    elif mode == "memory_leak":
        memory_leak()
    elif mode == "crash":
        crash()
    else:
        normal_operation()