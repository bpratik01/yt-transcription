# import os
# import whisper
# from src.config_loader import load_config
# import logging

# def transcribe_audio_files(audio_directory):
#     """Transcribes all audio files in the given directory using OpenAI's Whisper model (base)."""
#     logger = logging.getLogger(__name__)
    
#     # Load configuration from config.yaml
#     config = load_config()
#     output_directory = config.get('output_transcription_path', './transcripts')

#     logger.info(f"Starting transcription for audio files in {audio_directory}")
    
#     # Load the Whisper base model
#     model = whisper.load_model("base")

#     # Ensure the output directory exists
#     if not os.path.exists(output_directory):
#         os.makedirs(output_directory)
#         logger.debug(f"Created output transcription directory: {output_directory}")

#     # Iterate over all audio files in the directory
#     for audio_file in os.listdir(audio_directory):
#         if audio_file.endswith('.mp3'):  # Process only MP3 files
#             audio_path = os.path.join(audio_directory, audio_file)
#             try:
#                 logger.info(f"Transcribing: {audio_file}")
#                 result = model.transcribe(audio_path)

#                 # Save the transcription to a text file
#                 transcription_filename = os.path.splitext(audio_file)[0] + '.txt'
#                 transcription_path = os.path.join(output_directory, transcription_filename)
                
#                 with open(transcription_path, 'w') as f:
#                     f.write(result['text'])
                
#                 logger.info(f"Transcription saved for {audio_file} to {transcription_path}")
#             except Exception as e:
#                 logger.error(f"Failed to transcribe {audio_file}: {e}")


import os
import whisper
from src.config_loader import load_config
import logging

def transcribe_audio_files(audio_directory):
    """Transcribes all audio files in the given directory structure using OpenAI's Whisper model (base)."""
    logger = logging.getLogger(__name__)
    
    # Load configuration from config.yaml
    config = load_config()
    output_directory = config.get('output_transcription_path', './transcripts')

    logger.info(f"Starting transcription for audio files in {audio_directory}")
    
    # Load the Whisper base model
    model = whisper.load_model("base")

    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        logger.debug(f"Created output transcription directory: {output_directory}")

    # Iterate over all video folders in the directory
    for video_folder in os.listdir(audio_directory):
        video_path = os.path.join(audio_directory, video_folder)
        if os.path.isdir(video_path):
            chunks_folder = os.path.join(video_path, 'chunks')
            full_transcription = ""

            if os.path.exists(chunks_folder):
                # Process chunks if they exist
                chunks = [f for f in os.listdir(chunks_folder) if f.endswith('.mp3')]
                chunks.sort()  # Ensure chunks are processed in order
                
                logger.info(f"Found {len(chunks)} chunks for {video_folder}")
                for i, chunk in enumerate(chunks, 1):
                    chunk_path = os.path.join(chunks_folder, chunk)
                    try:
                        logger.info(f"Transcribing chunk {i}/{len(chunks)}: {chunk}")
                        result = model.transcribe(chunk_path)
                        full_transcription += result['text'] + "\n\n"
                        logger.debug(f"Chunk {i} transcription complete")
                    except Exception as e:
                        logger.error(f"Failed to transcribe {chunk}: {e}")
            else:
                # Process the single file if no chunks
                original_file = next((f for f in os.listdir(video_path) if f.endswith('.mp3')), None)
                if original_file:
                    original_path = os.path.join(video_path, original_file)
                    try:
                        logger.info(f"Transcribing single file: {original_file}")
                        result = model.transcribe(original_path)
                        full_transcription = result['text']
                        logger.debug("Single file transcription complete")
                    except Exception as e:
                        logger.error(f"Failed to transcribe {original_file}: {e}")
                else:
                    logger.warning(f"No MP3 file found in {video_path}")
                    continue

            # Save the full transcription to a text file
            transcription_filename = f"{video_folder}.txt"
            transcription_path = os.path.join(output_directory, transcription_filename)
            
            try:
                with open(transcription_path, 'w', encoding='utf-8') as f:
                    f.write(full_transcription)
                logger.info(f"Full transcription saved for {video_folder} to {transcription_path}")
            except Exception as e:
                logger.error(f"Failed to write transcription for {video_folder}: {e}")

    logger.info("Transcription process completed")