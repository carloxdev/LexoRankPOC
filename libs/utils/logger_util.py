# Python's Libraries
import logging

loggers = {}


class LoggerUtil(object):

    @classmethod
    def create(self, _environment):
        global loggers

        if loggers.get(_environment):
            return loggers.get(_environment)

        else:
            level = logging.INFO

            if _environment == "prod":
                level = logging.ERROR

            logging.root.handlers = []
            logging.basicConfig(
                format='[%(levelname)s] %(message)s',
                level=level
            )

            logger = logging.getLogger(_environment)
            loggers[_environment] = logger

            return logger


# LEVELS:
# - CRITICAL	50
# - ERROR	40
# - WARNING	30
# - INFO	20
# - DEBUG	10
# - NOTSET	0
