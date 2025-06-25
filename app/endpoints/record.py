# app/endpoints/record.py
from fastapi import APIRouter, HTTPException
from pipeline import run_pipeline  # if used, or your record_and_transcribe function
import sounddevice as sd
from scipy.io.wavfile import write
import whisper

router = APIRouter()

def record_and_transcribe(duration: int = 5, filename: str = "output.wav") -> str:
    fs = 44100
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
    except Exception as e:
        raise Exception(f"Error during recording: {e}")
    try:
        write(filename, fs, recording)
    except Exception as e:
        raise Exception(f"Error saving WAV file: {e}")
    try:
        w_model = whisper.load_model("medium")
    except Exception as e:
        raise Exception(f"Error loading Whisper model: {e}")
    try:
        result = w_model.transcribe(filename)
        return result["text"]
    except Exception as e:
        raise Exception(f"Error during transcription: {e}")

@router.get("/record")
def record_transcribe():
    try:
        transcription = record_and_transcribe(duration=5, filename="output.wav")
        return {"status": "success", "transcription": transcription}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
