from pydantic import BaseModel, DirectoryPath, FilePath, Field
from typing import List, Optional
from pathlib import Path


class SpeechRecognitionSettings(BaseModel):
    models_dir: DirectoryPath = Path("models/asr")
    enabled_languages: List[str] = []
    languages_metadata_path: FilePath = Path("data/languages/metadata.json")
    sample_rate: int = 16000
    n_mels: int = 80
    n_fft: int = 400
    hop_length: int = 160


class AppSettings(BaseModel):
    app_name: str = "LipiPala AI"
    version: str = "0.1.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 5000
    speech_recognition: SpeechRecognitionSettings = Field(
        default_factory=SpeechRecognitionSettings)
    # Add other service configs here, e.g., translation: TranslationSettings


# Global settings instance
settings = AppSettings()
