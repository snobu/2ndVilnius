"""
Azure Speech-to-Text client for making transcription requests.
"""

import json
import requests
from typing import List, Dict, Any, Optional, Union, BinaryIO
import os
from pathlib import Path

from config import AzureSpeechConfig


class AzureSpeechClient:
    """Client for Azure Speech-to-Text API."""
    
    def __init__(self, config: Optional[AzureSpeechConfig] = None):
        """
        Initialize the Azure Speech-to-Text client.
        
        Args:
            config (AzureSpeechConfig, optional): Configuration object.
                If not provided, a default config will be created.
        """
        self.config = config or AzureSpeechConfig()
    
    def transcribe(
        self, 
        audio_file: Union[str, Path, BinaryIO],
        locales: List[str] = ["en-US"],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Transcribe audio to text.
        
        Args:
            audio_file: Path to audio file or file-like object
            locales: List of language locales for transcription
            **kwargs: Additional parameters to pass to the API
        
        Returns:
            Dict containing the transcription response
        
        Raises:
            ValueError: If audio_file is invalid
            requests.RequestException: If the API request fails
        """
        # Prepare URL and headers
        url = self.config.transcribe_url
        headers = {
            "Ocp-Apim-Subscription-Key": self.config.api_key
        }
        
        # Prepare definition payload
        definition = {
            "locales": locales,
            **kwargs
        }
        
        # Prepare file for upload
        if isinstance(audio_file, (str, Path)):
            audio_path = Path(audio_file)
            if not audio_path.exists():
                raise ValueError(f"Audio file not found: {audio_path}")
            audio_data = open(audio_path, "rb")
        else:
            # Assume file-like object
            audio_data = audio_file
        
        try:
            # Prepare multipart/form-data
            files = {
                'audio': audio_data,
                'definition': (None, json.dumps(definition), 'application/json')
            }
            
            # Make the request
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()
            
            return response.json()
        
        finally:
            # Close file if we opened it
            if isinstance(audio_file, (str, Path)) and audio_data:
                audio_data.close()
    
    def get_supported_locales(self) -> Dict[str, Any]:
        """
        Get the list of supported locales for transcription.
        
        Returns:
            Dict containing the supported locales information
        """
        url = f"{self.config.base_url}/locales?api-version={self.config.api_version}"
        headers = {
            "Ocp-Apim-Subscription-Key": self.config.api_key
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()
