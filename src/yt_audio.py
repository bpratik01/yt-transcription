# import os
# import yt_dlp
# from src.config_loader import load_config
# import logging

# def download_channel_audio(channel_url, output_path):
#     """Download audio files from the given YouTube channel."""
#     logger = logging.getLogger(__name__)
#     logger.info(f"Starting download for channel: {channel_url}")
    
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#         'outtmpl': f'{output_path}/%(title)s.%(ext)s',
#         'ignoreerrors': True,
#         'no_warnings': True,
#         'quiet': True,
#         'extract_flat': False,
#         'playlistend': 5  # Limit to 5 videos for testing
#     }

#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             logger.debug(f"Downloading audio files to {output_path}")
#             ydl.download([channel_url])
#         logger.info(f"Download completed for channel: {channel_url}")
#     except Exception as e:
#         logger.error(f"Error downloading audio from {channel_url}: {e}")

#     # Check if files were actually downloaded
#     downloaded_files = os.listdir(output_path)
#     if downloaded_files:
#         logger.info(f"Downloaded {len(downloaded_files)} files to {output_path}")
#     else:
#         logger.warning(f"No files were downloaded to {output_path}")


import os
import yt_dlp
from pydub import AudioSegment
from src.config_loader import load_config
import logging

def split_audio(file_path, max_size_mb, output_directory=None):
    """
    Split an audio file into parts if it exceeds the specified size.
    
    :param file_path: Path to the audio file
    :param max_size_mb: Maximum size in MB for each part
    :param output_directory: Directory to save the split files (default: same as input file)
    :return: List of paths to the split audio files
    """
    logger = logging.getLogger(__name__)
    
    if output_directory is None:
        output_directory = os.path.dirname(file_path)
    
    audio = AudioSegment.from_mp3(file_path)
    duration_ms = len(audio)
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    
    if file_size_mb <= max_size_mb:
        return [file_path]
    
    num_parts = int(file_size_mb // max_size_mb) + 1
    part_duration_ms = duration_ms // num_parts
    
    split_files = []
    for i in range(num_parts):
        start_ms = i * part_duration_ms
        end_ms = (i + 1) * part_duration_ms if i < num_parts - 1 else duration_ms
        part = audio[start_ms:end_ms]
        
        part_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}_part{i+1}.mp3"
        part_path = os.path.join(output_directory, part_filename)
        part.export(part_path, format="mp3")
        split_files.append(part_path)
        
        logger.info(f"Created split part: {part_path}")
    
    return split_files

def download_and_process_channel_audio(channel_url, output_path):
    """Download audio files from the given YouTube channel, split if necessary, and organize into folders."""
    logger = logging.getLogger(__name__)
    logger.info(f"Starting download for channel: {channel_url}")
    
    config = load_config()
    max_file_size_mb = config.get('max_file_size_mb', 25)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'ignoreerrors': True,
        'no_warnings': True,
        'quiet': True,
        'extract_flat': False,
        'playlistend': 5  # Limit to 5 videos for testing
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.debug(f"Downloading audio files to {output_path}")
            ydl.download([channel_url])
        logger.info(f"Download completed for channel: {channel_url}")
    except Exception as e:
        logger.error(f"Error downloading audio from {channel_url}: {e}")
        return

    # Process downloaded files
    for filename in os.listdir(output_path):
        if filename.endswith('.mp3'):
            file_path = os.path.join(output_path, filename)
            video_name = os.path.splitext(filename)[0]
            
            # Create a folder for the video
            video_folder = os.path.join(output_path, video_name)
            os.makedirs(video_folder, exist_ok=True)
            
            # Move the original file to the video folder
            new_file_path = os.path.join(video_folder, filename)
            os.rename(file_path, new_file_path)
            
            # Split the audio if necessary
            chunks_folder = os.path.join(video_folder, 'chunks')
            os.makedirs(chunks_folder, exist_ok=True)
            
            split_files = split_audio(new_file_path, max_size_mb=max_file_size_mb, output_directory=chunks_folder)
            
            # Delete the original file if it was split
            if len(split_files) > 1:
                os.remove(new_file_path)
                logger.info(f"Deleted original file: {new_file_path}")
            
            logger.info(f"Processed {filename}: {'split into ' + str(len(split_files)) + ' chunks' if len(split_files) > 1 else 'kept original'} in {video_folder}")

    # Check if files were actually downloaded and processed
    processed_videos = [f for f in os.listdir(output_path) if os.path.isdir(os.path.join(output_path, f))]
    if processed_videos:
        logger.info(f"Processed {len(processed_videos)} videos in {output_path}")
    else:
        logger.warning(f"No videos were processed in {output_path}")
