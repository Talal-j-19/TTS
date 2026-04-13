# Google TTS FastAPI Service

A simple FastAPI application that converts text to speech using Google AI Studio API with AI-enhanced text processing.

## Features

- Convert text input to audio files (MP3)
- AI-powered text enhancement for better pronunciation
- Support for multiple languages
- RESTful API endpoints
- Automatic audio file generation and download
- Uses Google AI Studio API key for text processing
- Hybrid approach: AI Studio + gTTS for audio generation

## Prerequisites

1. Google AI Studio API key
2. Python 3.7+

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Google AI Studio API key:
```bash
# Set environment variable
set GOOGLE_AI_STUDIO_API_KEY=your_api_key_here
```

3. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET /
Health check endpoint

### POST /tts
Convert text to speech

**Request Body:**
```json
{
    "text": "Hello, world!",
    "language_code": "en-US",
    "voice_name": null,
    "voice_type": "standard",
    "audio_encoding": "mp3"
}
```

**Parameters:**
- `text` (required): Text to convert to speech
- `language_code` (optional): Language code (default: "en-US")
- `voice_name` (optional): Not used in this implementation (default: null)
- `voice_type` (optional): Voice type - only "standard" supported (default: "standard")
- `audio_encoding` (optional): Only "mp3" supported (default: "mp3")

**Response:**
```json
{
    "message": "Text-to-speech conversion successful",
    "audio_file_path": "tts_output_abc123.mp3"
}
```

### GET /download/{filename}
Download generated audio file

## Example Usage

### Using curl:
```bash
# Convert text to speech
curl -X POST "http://localhost:8000/tts" \
-H "Content-Type: application/json" \
-d '{"text": "Hello, world!", "language_code": "en-US"}'

# Download audio file (using the filename from response)
curl -O "http://localhost:8000/download/tts_output_abc123.mp3"
```

### Using Python requests:
```python
import requests

# Convert text to speech
response = requests.post(
    "http://localhost:8000/tts",
    json={"text": "Hello, world!", "language_code": "en-US"}
)
data = response.json()

# Download audio file
if data["audio_file_path"]:
    filename = data["audio_file_path"].split("/")[-1]
    audio_response = requests.get(f"http://localhost:8000/download/{filename}")
    
    with open(filename, "wb") as f:
        f.write(audio_response.content)
```

## Supported Languages

Common language codes (automatically mapped to gTTS format):
- `en-US` or `en-GB` - English
- `es-ES` - Spanish
- `fr-FR` - French
- `de-DE` - German
- `it-IT` - Italian
- `pt-BR` - Portuguese
- `ja-JP` - Japanese
- `ko-KR` - Korean
- `zh-CN` - Chinese (Simplified)

gTTS supports many more languages. See the [gTTS documentation](https://gtts.readthedocs.io/) for the complete list.

## How It Works

This application uses a hybrid approach:

1. **AI Text Enhancement**: Your text is first processed by Google AI Studio (Gemini Pro) to optimize pronunciation and flow
2. **Audio Generation**: The enhanced text is then converted to audio using Google's free TTS service (gTTS)
3. **Quality Enhancement**: The AI processing helps improve the naturalness of the final audio output

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- `400`: Bad request (invalid input)
- `404`: File not found
- `500`: Internal server error (TTS conversion issues)

## Notes

- Audio files are stored temporarily and will be cleaned up by the system
- Maximum text length is subject to both AI Studio and gTTS limits
- This uses Google AI Studio API for text processing and gTTS for audio generation
- AI enhancement may improve pronunciation but quality depends on the original text
- API key usage is subject to Google AI Studio pricing and quotas
