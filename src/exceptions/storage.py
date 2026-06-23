class StorageError(Exception):
    """Base exception class for all file storage operations."""

    pass


class StorageFileNotFoundError(StorageError):
    """Raised when the requested file does not exist on disk."""

    def __init__(self, file_key: str) -> None:
        self.file_key = file_key
        super().__init__(f'Requested file missing in storage: {file_key}')


class StorageAccessError(StorageError):
    """Raised when a file system permission or path restriction is violated."""

    def __init__(self, file_key: str, message: str) -> None:
        self.file_key = file_key
        super().__init__(f"Access error for key '{file_key}': {message}")
