# config_loader.py
import yaml
import logging

def load_config(config_file='config.yaml'):
    """Load configuration from a YAML file."""
    logger = logging.getLogger(__name__)
    logger.debug(f"Loading configuration from {config_file}")
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        logger.info(f"Configuration loaded successfully from {config_file}")
        return config
    except Exception as e:
        logger.error(f"Failed to load configuration from {config_file}: {e}")
        return None

# yt_audio.py

# whisper.py

# main.py
