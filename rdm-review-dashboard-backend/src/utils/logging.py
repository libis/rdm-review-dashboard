import logging
import time

from logging.handlers import TimedRotatingFileHandler
from persistence import filesystem
import os



def configure_logging(filename="backend.log"):
    filesystem.make_dir_if_not_exists(['logs'])
    log_path = os.path.join(*[*filesystem.BASE_DIR, 'logs', filename])
    logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[
                        logging.StreamHandler(),
                        TimedRotatingFileHandler(filename=log_path, when='midnight')
                    ])
