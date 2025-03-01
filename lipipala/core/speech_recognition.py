"""
Speech Recognition Module for LipiPala AI

This module provides functionality for automatic speech recognition (ASR)
specialized for endangered Indian languages.
"""

import os
import json
import logging
import numpy as np
from typing import Dict, List, Tuple, Optional, Union
from pathlib import Path

import torch
import torchaudio
import librosa

from lipipala.models.asr_model import ASRModel
from lipipala.preprocessing.audio import AudioPreprocessor

logger = logging.getLogger(__name__)


class SpeechRecognitionService:
    """
    Service for speech recognition of endangered Indian languages.

    This service handles the loading of ASR models for different languages,
    preprocessing of audio data, and transcription of speech to text.
    """

    def __init__(self, config: Dict):
        """
        Initialize the speech recognition service.

        Args:
            config: Configuration dictionary for the service
        """
        self.config = config
        self.models = {}
        self.preprocessor = AudioPreprocessor(
            sample_rate=config.get('sample_rate', 16000),
            n_mels=config.get('n_mels', 80),
            n_fft=config.get('n_fft', 400),
            hop_length=config.get('hop_length', 160)
        )

        # Load language metadata
        self.languages_metadata = self._load_languages_metadata()

        # Load models for enabled languages
        self._load_models()

        logger.info(
            f"Speech Recognition Service initialized with {len(self.models)} languages")

    def _load_languages_metadata(self) -> Dict:
        """
        Load metadata for all supported languages.

        Returns:
            Dictionary of language metadata keyed by language code
        """
        metadata_path = Path(self.config.get(
            'languages_metadata_path', 'data/languages/metadata.json'))

        if not metadata_path.exists():
            logger.warning(
                f"Languages metadata file not found at {metadata_path}, creating empty metadata")
            return {}

        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            logger.info(f"Loaded metadata for {len(metadata)} languages")
            return metadata
        except Exception as e:
            logger.error(f"Error loading languages metadata: {e}")
            return {}

    def _load_models(self):
        """Load ASR models for all enabled languages."""
        models_dir = Path(self.config.get('models_dir', 'models/asr'))
        enabled_languages = self.config.get('enabled_languages', [])

        # If no languages are explicitly enabled, try to load all available models
        if not enabled_languages and models_dir.exists():
            enabled_languages = [
                d.name for d in models_dir.iterdir() if d.is_dir()]

        for lang_code in enabled_languages:
            try:
                model_path = models_dir / lang_code / 'model.pt'
                config_path = models_dir / lang_code / 'config.json'

                if not model_path.exists() or not config_path.exists():
                    logger.warning(
                        f"Model files for language {lang_code} not found at {model_path}")
                    continue

                # Load model config
                with open(config_path, 'r', encoding='utf-8') as f:
                    model_config = json.load(f)

                # Initialize and load model
                model = ASRModel(model_config)
                model.load_state_dict(torch.load(
                    model_path, map_location='cpu'))
                model.eval()

                self.models[lang_code] = model
                logger.info(f"Loaded ASR model for language: {lang_code}")

            except Exception as e:
                logger.error(
                    f"Error loading model for language {lang_code}: {e}")

    def get_supported_languages(self) -> List[Dict]:
        """
        Get list of supported languages with metadata.

        Returns:
            List of dictionaries containing language information
        """
        supported = []

        for lang_code, model in self.models.items():
            lang_info = {
                'code': lang_code,
                'name': self.languages_metadata.get(lang_code, {}).get('name', lang_code),
                'family': self.languages_metadata.get(lang_code, {}).get('family', 'Unknown'),
                'script': self.languages_metadata.get(lang_code, {}).get('script', 'Unknown'),
                'endangerment_level': self.languages_metadata.get(lang_code, {}).get('endangerment_level', 'Unknown'),
                'regions': self.languages_metadata.get(lang_code, {}).get('regions', [])
            }
            supported.append(lang_info)

        return supported

    def transcribe(self, audio_path: Union[str, Path], language: str) -> Dict:
        """
        Transcribe audio file to text.

        Args:
            audio_path: Path to the audio file
            language: Language code for transcription

        Returns:
            Dictionary containing transcription results
        """
        if language not in self.models:
            raise ValueError(
                f"Language {language} is not supported for transcription")

        # Load and preprocess audio
        try:
            audio_data = self._load_audio(audio_path)
            features = self.preprocessor.process(audio_data)
        except Exception as e:
            logger.error(f"Error preprocessing audio: {e}")
            raise

        # Perform transcription
        model = self.models[language]

        with torch.no_grad():
            input_features = torch.from_numpy(
                features).unsqueeze(0)  # Add batch dimension
            outputs = model(input_features)
            transcription = model.decode(outputs)

        # Get language metadata
        lang_meta = self.languages_metadata.get(language, {})
        lang_name = lang_meta.get('name', language)

        return {
            'language': language,
            'language_name': lang_name,
            'text': transcription,
            'confidence': float(outputs.softmax(dim=-1).max().item()),
            'audio_duration': len(audio_data) / self.preprocessor.sample_rate
        }

    def _load_audio(self, audio_path: Union[str, Path]) -> np.ndarray:
        """
        Load and normalize audio file.

        Args:
            audio_path: Path to the audio file

        Returns:
            Numpy array of audio samples
        """
        audio_path = Path(audio_path)

        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        # Load audio with librosa to handle various formats
        audio_data, sr = librosa.load(
            audio_path, sr=self.preprocessor.sample_rate)

        # Normalize audio
        audio_data = librosa.util.normalize(audio_data)

        return audio_data

    def batch_transcribe(self, audio_paths: List[Union[str, Path]], language: str) -> List[Dict]:
        """
        Transcribe multiple audio files.

        Args:
            audio_paths: List of paths to audio files
            language: Language code for transcription

        Returns:
            List of dictionaries containing transcription results
        """
        results = []

        for audio_path in audio_paths:
            try:
                result = self.transcribe(audio_path, language)
                results.append(result)
            except Exception as e:
                logger.error(f"Error transcribing {audio_path}: {e}")
                results.append({
                    'language': language,
                    'error': str(e),
                    'audio_path': str(audio_path)
                })

        return results

    def is_healthy(self) -> bool:
        """
        Check if the service is healthy.

        Returns:
            Boolean indicating if the service is operational
        """
        # Service is healthy if at least one model is loaded
        return len(self.models) > 0

    def get_stats(self) -> Dict:
        """
        Get statistics for the speech recognition service.

        Returns:
            Dictionary of statistics
        """
        return {
            'models_loaded': len(self.models),
            'supported_languages': list(self.models.keys()),
            'preprocessor_config': {
                'sample_rate': self.preprocessor.sample_rate,
                'n_mels': self.preprocessor.n_mels
            }
        }
