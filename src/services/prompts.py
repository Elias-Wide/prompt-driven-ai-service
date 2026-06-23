from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional

from src.core.constants import META_PROMPT, VOICE_MODEL_PROMPT
from src.services.storage import FileStorageInterface


@dataclass(frozen=True)
class Prompt:
    """Represents an immutable prompt container.

    Holds a specific prompt identifier name and its textual content.
    """

    name: str
    text: str


class BasePromptRegistryService(ABC):
    """Abstract base class for discovering, caching, and serving prompts."""

    @abstractmethod
    def load_all_prompts(self) -> None:
        """Scan the storage source and cache items into memory."""
        pass

    @abstractmethod
    def get_prompt(self, prompt_name: str) -> str:
        """Fetch raw prompt text content by its core identifier."""
        pass

    @property
    @abstractmethod
    def meta_prompt(self) -> Optional[Prompt]:
        """Extract the baseline root core configuration model profile."""
        pass

    @property
    @abstractmethod
    def audio_prompt(self) -> Optional[Prompt]:
        """Extract the specific prompt container designed for audio processing."""
        pass

    @property
    @abstractmethod
    def get_extra_prompts(self) -> List[Prompt]:
        """Gather all indexed prompt configurations excluding root core blocks."""
        pass


class FilePromptRegistryService(BasePromptRegistryService):
    """Service for discovering, caching, and serving prompts via a FileStorageInterface."""

    def __init__(
        self,
        storage: FileStorageInterface,
        prompts_dir_prefix: str = 'prompts',
    ) -> None:
        """Initialize the registry with a storage engine and directory prefix.

        Args:
            storage: Instance implementing the FileStorageInterface contract.
            prompts_dir_prefix: The folder or prefix inside storage where prompts live.
        """
        if not storage:
            raise ValueError('The storage instance cannot be empty.')

        self.storage = storage
        self.prompts_dir_prefix = (
            prompts_dir_prefix
            if prompts_dir_prefix.endswith('/')
            else f'{prompts_dir_prefix}/'
        )
        self._registry: Dict[str, Prompt] = {}

    def load_all_prompts(self) -> None:
        """Scan the storage using the interface and cache Markdown files into memory."""
        self._registry.clear()

        try:
            all_files = self.storage.list_files(prefix=self.prompts_dir_prefix)
        except Exception as e:
            raise RuntimeError(
                f'Failed to scan storage at prefix {self.prompts_dir_prefix}'
            ) from e

        for file_key in all_files:
            if not file_key.endswith('.md'):
                continue

            try:
                raw_bytes = self.storage.get_file(file_key)
                raw_text = raw_bytes.decode('utf-8').strip()
                filename = file_key.split('/')[-1]
                prompt_key = filename[:-3]

                self._registry[prompt_key] = Prompt(
                    name=prompt_key, text=raw_text
                )
            except Exception:
                continue

    def get_prompt(self, prompt_name: str) -> str:
        """Fetch raw prompt text content by its core identifier."""
        if prompt_name.endswith('.md'):
            prompt_name = prompt_name[:-3]

        if prompt_name not in self._registry:
            raise KeyError(
                f"Prompt metadata key '{prompt_name}' is not registered in cache."
            )
        return self._registry[prompt_name].text

    @property
    def total_count(self) -> int:
        return len(self._registry)

    @property
    def meta_prompt(self) -> Optional[Prompt]:
        return self._registry.get(META_PROMPT)

    @property
    def audio_prompt(self) -> Optional[Prompt]:
        return self._registry.get(VOICE_MODEL_PROMPT)

    @property
    def get_extra_prompts(self) -> List[Prompt]:
        return [
            prompt
            for prompt in self._registry.values()
            if prompt.name not in (META_PROMPT, VOICE_MODEL_PROMPT)
        ]
