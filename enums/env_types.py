from enum import Enum


class EnvironmentTypes(Enum):
    """
        Enums used for identification of current environment and related settings.
        See config.json
    """
    LOCAL = 'LOCAL'
    DEV = 'DEV'
    TEST = 'TEST'
    PROD = 'PROD'
