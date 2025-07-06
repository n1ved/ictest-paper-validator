import main
from logger import logger, Logger


def check(pdf):
    return main.main(pdf, log=True)
