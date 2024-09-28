import logging

# create a logger
logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)

# create a file handler
file_handler = logging.FileHandler('mylog.log', mode='a')

# create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# add the file handler to the logger
logger.addHandler(file_handler)


