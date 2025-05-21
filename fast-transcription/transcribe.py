"""
Sample script demonstrating the usage of the Azure Speech-to-Text client.
"""

import argparse
import json
import sys
from pathlib import Path

import time
from config import AzureSpeechConfig
from speech_client import AzureSpeechClient
from utils import validate_audio_file, get_audio_duration


def main():
    """Main entry point for the sample script."""
    parser = argparse.ArgumentParser(description="Transcribe audio using Azure Speech-to-Text API")
    parser.add_argument("audio_file", help="Path to the audio file to transcribe")
    parser.add_argument("--locale", "-l", default="en-US", help="Locale for transcription (default: en-US)")
    parser.add_argument("--region", "-r", help="Azure region (overrides .env setting)")
    parser.add_argument("--api-key", "-k", help="API key (overrides .env setting)")
    parser.add_argument("--output", "-o", help="Output file for the transcription result")
    args = parser.parse_args()

    # Validate audio file
    audio_path = Path(args.audio_file)
    if not validate_audio_file(audio_path):
        print(f"Error: Invalid or non-existent audio file: {audio_path}", file=sys.stderr)
        sys.exit(1)
        
    # Calculate and display audio duration
    try:
        duration_seconds = get_audio_duration(audio_path)
        minutes, seconds = divmod(duration_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        if hours > 0:
            duration_str = f"{int(hours)}h {int(minutes)}m {seconds:.2f}s"
        elif minutes > 0:
            duration_str = f"{int(minutes)}m {seconds:.2f}s"
        else:
            duration_str = f"{seconds:.2f}s"
            
        print(f"Audio file duration: {duration_str} ({duration_seconds:.2f} seconds)")
    except Exception as e:
        print(f"Warning: Could not determine audio duration: {e}", file=sys.stderr)

    try:
        # Initialize configuration with optional overrides from command line
        config = AzureSpeechConfig(
            region=args.region,
            api_key=args.api_key
        )
        
        # Initialize client
        client = AzureSpeechClient(config)
        
        print(f"Transcribing audio file: {audio_path}")
        print(f"Using locale: {args.locale}")
        
        # Start timing the transcription process
        start_time = time.time()
        
        # Make the transcription request
        result = client.transcribe(
            audio_file=audio_path,
            locales=[args.locale]
        )
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        
        # Extract and handle combinedPhrases from the result
        combined_phrases = result.get("combinedPhrases", [])
        
        # Calculate speedup compared to realtime
        realtime_speedup = duration_seconds / elapsed_time if elapsed_time > 0 else 0
        
        # Format elapsed time and speedup nicely
        elapsed_str = f"{elapsed_time:.2f} seconds"
        print(f"Took {elapsed_str} to Fast Transcribe the input ({realtime_speedup:.1f}x realtime)")
        
        if args.output:
            with open(args.output, "w") as f:
                json.dump(combined_phrases, f, indent=2)
            print(f"Transcription result saved to: {args.output}")
        else:
            print("\nTranscription Result:")
            print(json.dumps(combined_phrases, indent=2))
            
    except ValueError as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error during transcription: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
