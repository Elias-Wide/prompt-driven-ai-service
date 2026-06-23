from abc import ABC, abstractmethod
from pathlib import Path

from src.exceptions.storage import StorageAccessError, StorageFileNotFoundError


class FileStorageInterface(ABC):
    """Abstract interface defining required contract for file operations."""

    @abstractmethod
    def save_file(self, file_bytes: bytes, filename: str) -> str:
        """Save raw bytes to the storage domain and return its path lookup."""
        pass

    @abstractmethod
    def get_file(self, file_key: str) -> bytes:
        """Retrieve binary file array content matching the provided key."""
        pass

    @abstractmethod
    def delete_file(self, file_key: str) -> None:
        """Remove a target file permanently from the storage ecosystem."""
        pass


class LocalDiskStorageService(FileStorageInterface):
    """Concrete implementation of file management using local server disk."""

    def __init__(self, upload_dir: Path) -> None:
        """Initialize and guarantee existence of target upload location."""
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def save_file(self, file_bytes: bytes, filename: str) -> str:
        file_path = self.upload_dir / filename
        try:
            file_path.write_bytes(file_bytes)
        except OSError as e:
            raise StorageAccessError(filename, f'Failed to write bytes: {e}')
        return str(file_path)

    def get_file(self, file_key: str) -> bytes:
        file_path = Path(file_key)
        if not file_path.exists():
            raise StorageFileNotFoundError(file_key)
        try:
            return file_path.read_bytes()
        except OSError as e:
            raise StorageAccessError(file_key, f'Failed to read bytes: {e}')

    def delete_file(self, file_key: str) -> None:
        file_path = Path(file_key)
        if not file_path.exists():
            raise StorageFileNotFoundError(file_key)
        try:
            file_path.unlink()
        except OSError as e:
            raise StorageAccessError(
                file_key, f'Failed to delete file: {e}'
            ) from e
