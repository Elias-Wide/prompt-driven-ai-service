from typing import Optional

from src.clients import BaseSpeechClient, BaseTextClient
from src.exceptions.ai import (
    AdditionalPromptMissingError,
    InvalidTokenError,
    MainPromptMissingError,
    TextAIResponseError,
    VoiceAIResponseError,
)
from src.exceptions.storage import StorageFileNotFoundError
from src.services.prompts import PromptRegistryService
from src.services.storage import FileStorageInterface


class AIService:
    """High-level orchestration service for AI text and speech processing."""

    def __init__(
        self,
        text_client: BaseTextClient,
        speech_client: BaseSpeechClient,
        prompt_service: PromptRegistryService,
        storage_service: FileStorageInterface,
    ):
        self.text_client = text_client
        self.speech_client = speech_client
        self._prompt_service = prompt_service
        self._storage_service = storage_service
        self._validate_prompts()

    def _validate_prompts(self) -> None:
        """Verify that all required system and prompts are present."""
        self._prompt_service.load_all_prompts()

        if not self._prompt_service.meta_prompt:
            raise MainPromptMissingError(
                'Critical configuration error: '
                'Baseline meta-prompt is missing.'
            )

        if not self._prompt_service.get_extra_prompts:
            raise AdditionalPromptMissingError(
                'Configuration error: Required auxiliary prompts are missing.'
            )

    def speech_to_text(self, audio_path: str) -> str:
        """Convert incoming audio file into a raw text string."""
        try:
            file = self._storage_service.get_file(audio_path)
        except StorageFileNotFoundError as e:
            raise VoiceAIResponseError(
                f'Audio file not found in storage: {audio_path}'
            ) from e
        try:
            transcription = self.speech_client.transcribe(file)
        except Exception as e:
            raise VoiceAIResponseError(
                f'Audio transcription layer failed: {str(e)}'
            ) from e

        if not transcription.strip():
            raise TextAIResponseError(
                'Aborted: Transcribed audio yielded an empty text sequence.'
            )

        return transcription

    def process_text_generation(self, prompt_text: str) -> str:
        """Send processed text to the LLM and return the generated content."""
        try:
            return self.text_client.send_request(prompt_text)
        except Exception as e:
            raise TextAIResponseError(
                f'Downstream language model pipeline failed: {str(e)}'
            ) from e

    def process_audio_pipeline(
        self, audio_path: str, auth_token: Optional[str] = None
    ) -> str:
        """Execute the full pipeline: token check, STT, and text processing."""
        if not auth_token:
            raise InvalidTokenError(
                'Access denied: Missing authentication token.'
            )

        transcription = self.speech_to_text(audio_path)
        return self.process_text_generation(transcription)
