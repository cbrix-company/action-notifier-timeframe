import logging


def pytest_configure(config):
    """Flake8 is very verbose by default. Silence it."""
    logger = logging.getLogger("flake8")
    logger.setLevel(logging.WARNING)
    logger.propagate = False
