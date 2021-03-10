from logger import get_logger
import logging

def test_get_logger() -> logging.Logger:
    logger = get_logger("test")
    assert type(logger) == logging.Logger