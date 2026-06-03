import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(
    name: str = "app",
    log_file: str = "logs/app.log",
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Configure a logger that writes to both stdout and a rotating log file.
    Returns the configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding handlers twice if this runs more than once
    # (e.g. Uvicorn reload, repeated imports)
    if logger.handlers:
        return logger

    # Don't bubble up to the root logger (prevents duplicate lines
    # alongside Uvicorn's own handlers)
    logger.propagate = False

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # --- stdout handler ---
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    # --- file handler (rotating, so it doesn't grow forever) ---
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)  # ensure logs/ exists

    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=10 * 1024 * 1024,   # 10 MB per file
        backupCount=5,               # keep 5 old files
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger