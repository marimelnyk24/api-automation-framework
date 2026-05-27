from loguru import logger
import sys
from datetime import datetime
from pathlib import Path


def get_project_root():
    return Path(__file__).resolve().parent.parent


def setup_logger():
    logger.remove()

    project_root = get_project_root()
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    log_file = logs_dir / f"test_run_{timestamp}.log"

    log_format = (
        "{time} | {level} | "
        "test={extra[test]} | "
        "test_module={extra[test_module]} | "
        "module={module} | "
        "function={function} | "
        "{message}"
    )

    logger.add(
        sys.stdout,
        format=log_format,
        level="INFO",
        colorize=True
    )

    logger.add(
        str(log_file),
        format=log_format,
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
        encoding="utf-8"
    )

    return logger