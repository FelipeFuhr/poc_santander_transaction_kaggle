import pickle
import yaml

def get_config():
    # Loads Configuration File
    try: 
        with open("config.yaml", "rb") as yaml_file:
            config = yaml.load(yaml_file, Loader=yaml.FullLoader)
            return config
    except (FileNotFoundError, pickle.UnpicklingError):
        logger.error("Could not load the application config file.")
        return {}