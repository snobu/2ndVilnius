"""
Utility functions for the Azure Speech-to-Text client.
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import wave
import contextlib
import mutagen


def validate_audio_file(file_path: str) -> bool:
    """
    Validate that the audio file exists and is likely a valid audio file.
    
    The Azure Speech-to-Text API requires that audio files:
    - Are shorter than 2 hours in audio duration
    - Are smaller than 200 MB in size
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        bool: True if file is valid, False otherwise
    """
    path = Path(file_path)
    
    # Check if file exists
    if not path.exists():
        return False
        
    # Check if it's a file
    if not path.is_file():
        return False
        
    # Check supported audio file extensions
    audio_extensions = [
        '.wav',      # WAV, including ALAW and MULAW in WAV containers
        '.mp3',      # MP3
        '.opus',     # OPUS
        '.ogg',      # OGG
        '.flac',     # FLAC
        '.wma',      # WMA
        '.aac',      # AAC
        '.amr',      # AMR
        '.webm',     # WebM
        '.m4a',      # M4A
        '.spx'       # SPEEX
    ]
    if path.suffix.lower() not in audio_extensions:
        return False
        
    # Check if file is not empty
    if path.stat().st_size == 0:
        return False
    
    # Check file size (must be less than 200 MB)
    max_size_bytes = 200 * 1024 * 1024  # 200 MB in bytes
    if path.stat().st_size > max_size_bytes:
        return False
    
    # Check audio duration (must be less than 2 hours)
    try:
        duration = get_audio_duration(path)
        max_duration = 2 * 60 * 60  # 2 hours in seconds
        if duration > max_duration:
            return False
    except Exception:
        # If we can't determine the duration, we'll assume it's valid
        # and let the API handle any potential issues
        pass
        
    return True


def format_transcription_result(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format the raw transcription response to extract useful information.
    
    Args:
        response: Raw API response from the transcription API
        
    Returns:
        Dict containing formatted transcription results
    """
    # This function can be expanded based on the actual API response structure
    # For now, it just returns the original response
    return response


def get_default_audio_path() -> Optional[Path]:
    """
    Get the default audio file path from the environment.
    
    Returns:
        Path to default audio file or None if not set
    """
    audio_path = os.getenv("DEFAULT_AUDIO_PATH")
    if audio_path and Path(audio_path).exists():
        return Path(audio_path)
    return None


def get_audio_duration(file_path: Path) -> float:
    """
    Get the duration of an audio file in seconds.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        float: Duration of the audio file in seconds
        
    Raises:
        Exception: If the duration cannot be determined
    """
    extension = file_path.suffix.lower()
    
    # Handle WAV files
    if extension == '.wav':
        with contextlib.closing(wave.open(str(file_path), 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration
    
    # Handle other audio formats using mutagen
    else:
        try:
            audio = mutagen.File(file_path)
            if audio is not None and hasattr(audio, 'info') and hasattr(audio.info, 'length'):
                return float(audio.info.length)
            raise Exception("Could not determine audio duration")
        except Exception as e:
            raise Exception(f"Error determining audio duration: {e}")
