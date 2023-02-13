import logging

logging.basicConfig(format='%(asctime)s %(levelname)s [%(filename)s:%(lineno)d %(funcName)s()] [%(message)s]', filename='logs/logs.log', encoding='utf-8',
                    level=logging.DEBUG,
                    datefmt='%d-%m-%Y %I:%M:%S %p')