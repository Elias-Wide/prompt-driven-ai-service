from pathlib import Path
from typing import Optional

from src.core.exceptions import (
    AdditionalPromptMissingError,
    InvalidTokenError,
    MainPromptMissingError,
    TextAIResponseError,
    VoiceAIResponseError,
)
from src.services.ai_clients import BaseSpeechClient, BaseTextClient
from src.services.prompt_registry import PromptRegistryService


class AIService:
    """High-level orchestration service for AI text and speech processing."""

    def __init__(
        self,
        text_client: BaseTextClient,
        speech_client: BaseSpeechClient,
        prompt_service: PromptRegistryService,
    ):
        self.text_client = text_client
        self.speech_client = speech_client
        self._prompt_service = prompt_service
        self._validate_prompts()

    def _validate_prompts(self) -> None:
        """Verify that all required system and auxiliary prompts are present."""
        self._prompt_service.load_all_prompts()

        if not self._prompt_service.meta_prompt:
            raise MainPromptMissingError(
                "Critical configuration error: Baseline meta-prompt is missing."
            )

        if not self._prompt_service.get_extra_prompts:
            raise AdditionalPromptMissingError(
                "Configuration error: Required auxiliary prompts are missing."
            )

    def speech_to_text(self, audio_path: str) -> str:
        """Convert incoming audio file into a raw text string."""
        if not Path(audio_path).is_file():
            raise VoiceAIResponseError(
                f"Audio processing aborted: File not found at {audio_path}"
            )

        try:
            transcription = self.speech_client.transcribe(audio_path)
        except Exception as error:
            raise VoiceAIResponseError(
                f"Audio transcription layer failed: {str(error)}"
            )

        if not transcription.strip():
            raise TextAIResponseError(
                "Aborted: Transcribed audio yielded an empty text sequence."
            )

        return transcription

    def process_text_generation(self, prompt_text: str) -> str:
        """Send processed text to the LLM and return the generated content."""
        try:
            return self.text_client.send_request(prompt_text)
        except Exception as error:
            raise TextAIResponseError(
                f"Downstream language model pipeline failed: {str(error)}"
            )

    def process_audio_pipeline(
        self, audio_path: str, auth_token: Optional[str] = None
    ) -> str:
        """Execute the full pipeline: token check, STT, and text processing."""
        if not auth_token:
            raise InvalidTokenError("Access denied: Missing authentication token.")

        transcription = self.speech_to_text(audio_path)
        return self.process_text_generation(transcription)
