import abc
from pathlib import Path


class FileStorageInterface(abc.ABC):
    """Abstract interface defining required contract for file operations."""

    @abc.abstractmethod
    def save_file(self, file_bytes: bytes, filename: str) -> str:
        """Save raw bytes to the storage domain and return its path lookup."""
        pass

    @abc.abstractmethod
    def get_file(self, file_key: str) -> bytes:
        """Retrieve binary file array content matching the provided key."""
        pass

    @abc.abstractmethod
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
        file_path.write_bytes(file_bytes)
        return str(file_path)

    def get_file(self, file_key: str) -> bytes:
        file_path = Path(file_key)
        if not file_path.exists():
            raise FileNotFoundError(f"Requested file missing: {file_key}")
        return file_path.read_bytes()

    def delete_file(self, file_key: str) -> None:
        file_path = Path(file_key)
        if file_path.exists():
            file_path.unlink()
