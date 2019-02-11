from datetime import timedelta


# This will not affect gunicorn config
HOST = '0.0.0.0'
PORT = 5000

DEBUG = False
PROPAGATE_EXCEPTIONS = True

JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=15)

LOGCONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'request': {
            '()': 'logging.Formatter',
            'format': '[%(asctime)s]: %(message)s'
        },
        'standard': {
            '()': 'logging.Formatter',
            'format': '[%(levelname)s] [%(asctime)s]: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'stream': 'ext://sys.stderr'
        },
        'request': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/requests.log',
            'mode': 'a', 
            'maxBytes': 5*1024*1024,
            'backupCount': 5,
            'formatter': 'request'
        },
        'app': {
            'class': 'logging.FileHandler',
            'filename': 'logs/app.log',
            'mode': 'w',
            'formatter': 'standard'
        },
        'error': {
            'class': 'logging.FileHandler',
            'filename': 'logs/errors.log',
            'mode': 'w',
            'formatter': 'standard'
        }
    },
    'loggers': {
        'app': {
            'handlers': ['console', 'app'],
            'level': 'DEBUG'
        },
        'flask.request': {
            'handlers': ['request'],
            'level': 'INFO'
        },
        'flask.error': {
            'handlers': ['console', 'app', 'error'],
            'level': 'ERROR'
        }
    }
}

LOGCONFIG_QUEUE = ['flask.request']
LOGCONFIG_REQUESTS_ENABLED = True
LOGCONFIG_REQUESTS_LOGGER = 'flask.request'
LOGCONFIG_REQUESTS_LEVEL = logging.INFO
