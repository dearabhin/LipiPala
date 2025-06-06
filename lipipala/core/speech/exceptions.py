class SpeechServiceError(Exception):
    """Base exception for the speech service."""
    pass


class LanguageNotSupportedError(SpeechServiceError):
    """Raised when a requested language model is not available."""
    pass


class AudioProcessingError(SpeechServiceError):
    """Raised during audio loading or feature extraction."""
    pass


class ModelLoadError(SpeechServiceError):
    """Raised when a model file cannot be loaded."""
    pass
