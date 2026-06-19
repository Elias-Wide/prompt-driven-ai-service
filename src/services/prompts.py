from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from src.core.config import PROMPTS_DIR
from src.core.constants import META_PROMPT


@dataclass(frozen=True)
class Prompt:
    """Represents an immutable prompt container.

    Holds a specific prompt identifier name and its textual content.
    """

    name: str
    text: str


class PromptRegistryService:
    """Service for discovering, caching, and serving prompts from files."""

    def __init__(self, prompts_dir: Path = PROMPTS_DIR) -> None:
        """Initialize the registry with a target prompts directory.

        Args:
            prompts_dir: Path pointing to the directory with files.

        Raises:
            ValueError: If the provided path evaluates to empty.
            FileNotFoundError: If the designated location does not exist.
        """
        if not prompts_dir:
            raise ValueError('The prompts directory path cannot be empty.')
        if not prompts_dir.exists():
            raise FileNotFoundError(
                f'Provided prompts directory does not exist: {prompts_dir}'
            )
        self.prompts_dir = prompts_dir
        self._registry: Dict[str, Prompt] = {}

    def load_all_prompts(self) -> None:
        """Scan the flat prompts directory and cache files into memory.

        Raises:
            FileNotFoundError: If the base directory missing from disk.
        """
        if not self.prompts_dir.exists():
            raise FileNotFoundError(
                f'Base prompts directory missing: {self.prompts_dir}'
            )
        self._registry.clear()
        for file_path in self.prompts_dir.glob('*.md'):
            if not file_path.is_file():
                continue
            prompt_key = file_path.stem
            raw_text = file_path.read_text(encoding='utf-8').strip()
            self._registry[prompt_key] = Prompt(name=prompt_key, text=raw_text)

    def get_prompt(self, prompt_name: str) -> str:
        """Fetch raw prompt text content by its core filename identifier.

        Args:
            prompt_name: Name of the target file with or without extension.

        Returns:
            The extracted prompt content string.

        Raises:
            KeyError: If the designated key is missing from memory registry.
        """
        if prompt_name.endswith('.md'):
            prompt_name = prompt_name[:-3]
        if prompt_name not in self._registry:
            raise KeyError(
                f"Prompt metadata key '{prompt_name}' is not registered."
            )
        return self._registry[prompt_name].text

    @property
    def total_count(self) -> int:
        """Get the current count of loaded prompts within memory cache.

        Returns:
            Total absolute integer counter metric.
        """
        return len(self._registry)

    @property
    def meta_prompt(self) -> Optional[Prompt]:
        """Extract the baseline root core configuration model profile.

        Returns:
            The primary system setup blueprint if found, otherwise None.
        """
        return self._registry.get(META_PROMPT)

    @property
    def get_extra_prompts(self) -> List[Prompt]:
        """Gather all indexed prompt configurations excluding root core block.

        Returns:
            A list containing extra instructional data nodes.
        """
        return [
            prompt
            for prompt in self._registry.values()
            if prompt.name != META_PROMPT
        ]
