from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from src.core.config import PROMPTS_DIR
from src.core.constants import META_PROMPT


@dataclass(frozen=True)
class Prompt:
    name: str
    text: str


class PromptRegistryService:
    def __init__(self, prompts_dir: Path = PROMPTS_DIR) -> None:
        if not prompts_dir:
            raise ValueError('The prompts directory path cannot be empty.')
        if not prompts_dir.exists():
            raise FileNotFoundError(
                f'Provided prompts directory does not exist: {prompts_dir}'
            )
        self.prompts_dir = prompts_dir
        self._registry: Dict[str, Prompt] = {}

    def load_all_prompts(self) -> None:
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
        if prompt_name.endswith('.md'):
            prompt_name = prompt_name[:-3]
        if prompt_name not in self._registry:
            raise KeyError(
                f"Prompt metadata key '{prompt_name}' is not registered."
            )
        return self._registry[prompt_name].text

    @property
    def total_count(self) -> int:
        return len(self._registry)

    @property
    def meta_prompt(self) -> Optional[Prompt]:
        return self._registry.get(META_PROMPT)

    @property
    def get_extra_prompts(self) -> List[Prompt]:
        return [
            prompt
            for prompt in self._registry.values()
            if prompt.name != META_PROMPT
        ]
