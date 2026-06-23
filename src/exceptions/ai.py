class AIServiceError(Exception):
    """Base exception for all AI service-related errors."""

    def __init__(
        self,
        message: str = 'Internal AI service error',
        status_code: int = 500,
    ):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class InvalidTokenError(AIServiceError):
    """Raised when the provided authentication token is invalid or expired."""

    def __init__(self, message: str = 'Invalid or expired token provided'):
        super().__init__(message, status_code=401)


class PromptMissingError(AIServiceError):
    """Base exception for cases where mandatory input prompts are missing."""

    def __init__(self, message: str = 'Required prompt is missing'):
        super().__init__(message, status_code=400)


class MainPromptMissingError(PromptMissingError):
    """Raised when the primary system or user prompt is missing."""

    def __init__(self, message: str = 'Main prompt is required'):
        super().__init__(message)


class AudioPromptMissingError(PromptMissingError):
    """Raised when the prompt for audio model transcription is missing."""

    def __init__(
        self, message: str = 'Audio transcription prompt is required'
    ):
        super().__init__(message)


class AdditionalPromptMissingError(PromptMissingError):
    """Raised when auxiliary prompts or context data are missing."""

    def __init__(self, message: str = 'Additional prompts are missing'):
        super().__init__(message)


class AIResponseError(AIServiceError):
    """Base exception for downstream AI generation and processing failures."""

    def __init__(self, message: str = 'AI generation failed'):
        super().__init__(message, status_code=502)


class TextAIResponseError(AIResponseError):
    """Raised when the text model generates an invalid response."""

    def __init__(
        self, message: str = 'Text model returned an invalid response'
    ):
        super().__init__(message)


class VoiceAIResponseError(AIResponseError):
    """Raised when voice synthesis (TTS) or audio processing fails."""

    def __init__(self, message: str = 'Voice synthesis or processing failed'):
        super().__init__(message)
