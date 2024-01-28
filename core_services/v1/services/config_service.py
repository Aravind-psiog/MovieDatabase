from dotenv import load_dotenv
import os





def load_config():
    """
    Load Config
    -----------

    Thus function loads config data from the environment

    Attributes: None

    Returns: Config data
    """
    config = load_dotenv("./configs/staging.env")
    return config
