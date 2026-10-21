import logging
from datetime import date

def setup_log():
    logging.basicConfig(
        filename= f"output/log_{date.today()}.log",
        level= logging.INFO,
        encoding= "utf-8",
        format= "%(asctime)s %(levelname)s %(message)s",
    )

def log_info(message):
    logging.info(message)
def log_error(message):
    logging.error(message)
