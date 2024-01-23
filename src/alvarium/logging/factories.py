import logging
import socket


class LoggerFactory:
    """A factory that returns a specific implementation of a Logger"""

    def get_logger(self, name: str = __name__, level: int = logging.DEBUG) -> logging.Logger:
        class LowerCaseLevelNameFormatter(logging.Formatter):
            def format(self, record):
                record.levelname = record.levelname.lower()
                return super().format(record)
            
        logger = logging.getLogger(name)
        logger.propagate = False
        logging.basicConfig(level=level)

        handler = logging.StreamHandler()
        formatter = LowerCaseLevelNameFormatter('{"timestamp":"%(asctime)s","log-level": "%(levelname)s","message":"%(message)s","hostname":"%(hostname)s", "application":"%(filename)s", "line-number":"%(filename)s:%(lineno)d"}', 
                                      datefmt='%Y-%m-%dT%H:%M:%SZ',
                                      validate=True, 
                                      defaults={'hostname': socket.gethostname()} )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger