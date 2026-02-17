import logging
import sys

def setup_logging(level=logging.INFO) -> None:
    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)

    # Replace handlers to avoid duplicate logs
    if root.handlers:
        root.handlers[:] = [handler]
    else:
        root.addHandler(handler)
