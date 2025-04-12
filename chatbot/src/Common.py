'''
************************************************************************************************

* File Name         : Common.py
* Description       : Functions related to common operations
* Created By        : Vidushi Gandhi
* Date              : 9th April 2025

************************************************************************************************

'''

# Import Modules
from pathlib import Path
import os
import yaml

def _read_chatbot_config():
    config_path = os.path.join(Path(__file__).resolve().parent.parent.parent, 'config')
    with open(config_path + '/config.yaml') as fh:
        chat_config = yaml.load(fh, Loader=yaml.FullLoader)
    return chat_config


def chat_bot_config():
    chat_config = _read_chatbot_config()
    return chat_config['ChatBot']


def portfolio_config():
    chat_config = _read_chatbot_config()
    return chat_config['Portfolio']


def model_config():
    chat_config = _read_chatbot_config()
    return chat_config['AIModel'] 


def db_config():
    chat_config = _read_chatbot_config()
    return chat_config['DBConfig'] 