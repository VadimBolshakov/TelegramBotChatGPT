import logging.config
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
LOG_FILE = os.getenv('LOG_FILE')


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(asctime)s:%(levelname)s] %(message)s, func=%(funcName)s, file=%(filename)s, %(pathname)s'
        },
        'short_formatter': {
            'format': '[%(asctime)s:%(levelname)s] %(message)s '
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'short_formatter',
            'level': 'ERROR',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default_formatter',
            'level': 'INFO',
            'filename': LOG_FILE,
            'maxBytes': 32768,
            'backupCount': 5
        },
        'email': {
            'class': 'logging.handlers.SMTPHandler',
            'mailhost': 'localhost',
            'fromaddr': 'my_app@domain.tld',
            'toaddrs': '- support_team@domain.tld',
            'subject': 'Houston, we have a problem',
            'level': 'ERROR',
        },

    },
    'loggers': {
        'my_logger': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('my_logger')


if __name__ == '__main__':
    logger.debug('debug log')
    logger.info('logger info')
    logger.warning('warning')
    logger.error('ZeroDivisionError', exc_info=True)
    logger.exception('exception')
    logger.critical('critical')

    logging.debug('debug log')
    logging.info('logger info')
    logging.warning('warning')
    logging.error('ZeroDivisionError', exc_info=True)
    logging.exception('exception')
    logging.critical('critical')
