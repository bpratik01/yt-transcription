# import os
# from src.yt_audio import download_channel_audio
# from src.whisper import transcribe_audio_files
# from src.config_loader import load_config
# import logging

# def run_pipeline():
#     """Complete workflow: download audio from YouTube and transcribe using Whisper."""
#     logging.basicConfig(level=logging.INFO)
#     logger = logging.getLogger(__name__)
#     logger.info("Pipeline started")

#     # Step 1: Load configuration from config.yaml
#     config = load_config()

#     if not config:
#         logger.error("Failed to load configuration. Exiting pipeline.")
#         return

#     # Step 2: Extract values from config
#     channel_link = config.get('channel_link')
#     audio_save_path = config.get('save_path', './downloaded_audio')

#     # Ensure the output directory exists
#     os.makedirs(audio_save_path, exist_ok=True)

#     # Step 3: Download all videos from the channel as audio
#     logger.info(f"Downloading audio from channel: {channel_link}")
#     download_channel_audio(channel_link, audio_save_path)

#     # Step 4: Transcribe the downloaded audio files
#     logger.info(f"Starting transcription for audio files in: {audio_save_path}")
#     transcribe_audio_files(audio_save_path)

#     logger.info("Pipeline completed successfully")

# if __name__ == '__main__':
#     run_pipeline()


import os
from src.yt_audio import download_and_process_channel_audio
from src.whisper import transcribe_audio_files
from src.config_loader import load_config
import logging

def run_pipeline():
    """Complete workflow: download audio from YouTube, split if necessary, and transcribe using Whisper."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Pipeline started")

    # Step 1: Load configuration from config.yaml
    config = load_config()

    if not config:
        logger.error("Failed to load configuration. Exiting pipeline.")
        return

    # Step 2: Extract values from config
    channel_link = config.get('channel_link')
    audio_save_path = config.get('save_path', './downloaded_audio')

    # Ensure the output directory exists
    os.makedirs(audio_save_path, exist_ok=True)

    # Step 3: Download all videos from the channel as audio and process them
    logger.info(f"Downloading and processing audio from channel: {channel_link}")
    download_and_process_channel_audio(channel_link, audio_save_path)

    # Step 4: Transcribe the downloaded audio files
    logger.info(f"Starting transcription for audio files in: {audio_save_path}")
    transcribe_audio_files(audio_save_path)

    logger.info("Pipeline completed successfully")

if __name__ == '__main__':
    run_pipeline()
