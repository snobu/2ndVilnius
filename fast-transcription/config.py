"""
Configuration module for Azure Speech-to-Text client.
Loads environment variables from .env file.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class AzureSpeechConfig:
    """Configuration class for Azure Speech-to-Text API."""
    
    def __init__(self, region=None, api_key=None, api_version="2024-11-15"):
        """
        Initialize configuration with API credentials.
        
        Args:
            region (str, optional): Azure region. Defaults to env var AZURE_SPEECH_REGION.
            api_key (str, optional): API subscription key. Defaults to env var AZURE_SPEECH_KEY.
            api_version (str, optional): API version. Defaults to "2024-11-15".
        """
        self.region = region or os.getenv("AZURE_SPEECH_REGION")
        self.api_key = api_key or os.getenv("AZURE_SPEECH_KEY")
        self.api_version = api_version
        
        if not self.region or not self.api_key:
            raise ValueError(
                "Azure Speech API credentials not found. "
                "Please provide region and api_key or set AZURE_SPEECH_REGION and AZURE_SPEECH_KEY environment variables."
            )
    
    @property
    def base_url(self):
        """Get the base URL for API requests."""
        return f"https://{self.region}.api.cognitive.microsoft.com/speechtotext"
    
    @property
    def transcribe_url(self):
        """Get the URL for transcription requests."""
        return f"{self.base_url}/transcriptions:transcribe?api-version={self.api_version}"
