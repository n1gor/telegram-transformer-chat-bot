import os

import jsonpickle

from enums.env_types import EnvironmentTypes
from configs.config import DevConfig  # , ProdConfig
from google.oauth2 import service_account


def read_config():
    """
    Read data from configuration files
    If we can't read data from config then it's better not to start application
    """
    relative_path_to_file = os.path.join('configs', 'config.json')
    full_path_to_file = os.path.join(os.path.dirname(__file__), relative_path_to_file)
    with open(full_path_to_file) as file_data:
        data = file_data.read()
        initial_config = jsonpickle.decode(data)
        initial_config_type = initial_config['ENV_TYPE']
    if initial_config_type == EnvironmentTypes.LOCAL.value:
        config_data = 'N/A'
    elif initial_config_type == EnvironmentTypes.DEV.value:
        config_data = DevConfig()
    elif initial_config_type == EnvironmentTypes.TEST.value:
        config_data = 'N/A'
    # elif initial_config_type == EnvironmentTypes.PROD.value:
    #     config_data = ProdConfig()
    else:
        config_data = 'N/A'
    return config_data


def read_credentials_data():
    relative_path_to_file = os.path.join('configs', 'creds.json')
    full_path_to_file = os.path.join(os.path.dirname(__file__), relative_path_to_file)
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    credentials = service_account.Credentials.from_service_account_file(full_path_to_file, scopes=scope)
    return credentials
