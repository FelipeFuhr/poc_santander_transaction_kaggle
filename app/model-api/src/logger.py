import logging

def get_logger(name):
    ''' 
    Gets our custom logger for this instance.
    It sets the app.log file level to DEBUG  (so every message above DEBUG 
    will be forwarded to the file) and the stream to INFO. 

    INPUT:
    - input: name: module name
    OUTPUT:
    - output: logger
    '''

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # Sets the File Handler
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Sets the Stream Handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    # Adds handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger