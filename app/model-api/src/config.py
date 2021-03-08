"""
Reads Configuration from config.yaml
"""
import yaml

def get_config() -> dict:
    """
    Try to read Configuration File
    """
    try: 
        with open("config.yaml", "rb") as yaml_file:
            config = yaml.load(yaml_file, Loader=yaml.FullLoader)
            return config
    except (FileNotFoundError):
        logger.error("Could not load the application config file.")
        return {}