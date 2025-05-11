'''
************************************************************************************************
    
    FileName          : chat_log.py
    Description       : File handle app logs
    Created By        : Vidushi Gandhi
    Date              : 27 April 2025

************************************************************************************************
'''

# Import Modules 
import os
from logging.handlers import RotatingFileHandler


def get_logging_config(BASE_DIR):
    log_dir = os.path.join(BASE_DIR, 'chat_logs')
    os.makedirs(log_dir, exist_ok=True)  # Make sure log folder exists

    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '[{asctime}] {levelname} [{name}] {message}',
                'style': '{',
            },
        },
        'handlers': {
            'info_file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(log_dir, 'chat_info.log'),
                'formatter': 'verbose',
                'maxBytes': 5*1024*1024,
                'backupCount': 3,
            },
            'error_file': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(log_dir, 'chat_error.log'),
                'formatter': 'verbose',
                'maxBytes': 5*1024*1024,
                'backupCount': 3,
            },
            'debug_file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(log_dir, 'chat_debug.log'),
                'formatter': 'verbose',
                'maxBytes': 5*1024*1024,
                'backupCount': 3,
            },
        },
        'loggers': {
            'django': {
                'handlers': ['info_file', 'error_file'],
                'level': 'INFO',
                'propagate': True,
            },
            'app_logger': {
                'handlers': ['info_file', 'error_file', 'debug_file'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
    }
