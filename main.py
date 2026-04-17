from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai
from google.genai import types
import os
import tempfile
import wave
from typing import Optional
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Google TTS API",
    description="Convert text to speech using Google AI Studio TTS API"
)

class TTSRequest(BaseModel):
    text: str
    voice_name: Optional[str] = None


class TTSResponse(BaseModel):
    message: str
    audio_file_path: Optional[str] = None

def save_wav_file(filename, pcm_data, channels=1, rate=24000, sample_width=2):
    """Save PCM audio data to WAV file"""
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm_data)

@app.get("/")
async def root():
    return {"message": "Google AI Studio TTS API is running"}

@app.post("/tts", response_model=TTSResponse)
async def text_to_speech(request: TTSRequest):
    try:
        # Get API key from environment
        api_key = os.getenv("GOOGLE_AI_STUDIO_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="GOOGLE_AI_STUDIO_API_KEY not found in environment variables"
            )
        
        # Initialize client
        client = genai.Client(api_key=api_key)
        
        # Set voice configuration
        voice_config = types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name=request.voice_name or "Kore"
            )
        )
        
        # Generate content with TTS
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=request.text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=voice_config
                )
            )
        )
        
        # Get the audio data
        audio_data = response.candidates[0].content.parts[0].inline_data.data
        
        # Create a temporary file to store the audio
        temp_dir = tempfile.gettempdir()
        filename = f"tts_output_{uuid.uuid4().hex}.wav"
        audio_file_path = os.path.join(temp_dir, filename)
        
        # Save the audio content to WAV file
        save_wav_file(audio_file_path, audio_data)
        
        return TTSResponse(
            message="Text-to-speech conversion successful using Google AI Studio",
            audio_file_path=audio_file_path
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during text-to-speech conversion: {str(e)}"
        )

@app.get("/download/{filename}")
async def download_audio(filename: str):
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="audio/mpeg" if filename.endswith(".mp3") else "audio/ogg"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5035)
