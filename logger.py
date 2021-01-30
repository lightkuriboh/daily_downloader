import logging

urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.CRITICAL)


class LoggerConfig:
    LOGGING_DIR = 'logs/'
    MAIN_LOG_FILE = ''.join([LOGGING_DIR, 'main.logs'])
    LOG_FILE_MODE = 'a'
    LOG_DATE_FORMAT = '%y-%m-%d %H:%M'
    PRIVATE_LOG_FORMAT = '%(asctime)s %(name)-24s %(levelname)-8s %(message)s'
    PUBLIC_LOG_FORMAT = '%(asctime)s: %(levelname)-8s %(message)s'


class Logger:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format=LoggerConfig.PRIVATE_LOG_FORMAT,
                            datefmt=LoggerConfig.LOG_DATE_FORMAT,
                            filename=LoggerConfig.MAIN_LOG_FILE,
                            filemode=LoggerConfig.LOG_FILE_MODE)
        self.logger = logging.getLogger()

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)


class PublicLogger(Logger):
    def __init__(self):
        super().__init__()
        console = logging.StreamHandler()
        console.setLevel(logging.WARNING)
        formatter = logging.Formatter(LoggerConfig.PUBLIC_LOG_FORMAT)
        console.setFormatter(formatter)

        self.logger.addHandler(console)
