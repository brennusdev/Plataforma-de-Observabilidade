import time
import psutil


BOOT_TIME = psutil.boot_time()


def collect_system_metrics() -> dict:
    disk = psutil.disk_usage("/")

    return {
        "cpu_percent": psutil.cpu_percent(interval=0.2),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": disk.percent,
        "uptime_seconds": time.time() - BOOT_TIME,
    }
