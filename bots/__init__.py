import logging

from config_reader import read_config

config_data = read_config()

logging.basicConfig(filename='logs.log', level=logging.DEBUG,
                    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
