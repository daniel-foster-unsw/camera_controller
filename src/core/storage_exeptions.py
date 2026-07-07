"""
storage_exceptions.py

Custom exceptions for the storage subsystem.
"""


class StorageError(Exception):
    """
    Base exception for all storage-related errors.
    """
    pass


class StorageInitialisationError(StorageError):
    """
    Raised when the storage system cannot be initialised.
    """
    pass


class StoragePathError(StorageError):
    """
    Raised when the configured storage path is invalid or inaccessible.
    """
    pass


class StorageWriteError(StorageError):
    """
    Raised when an image or file cannot be written to disk.
    """
    pass


class StorageReadError(StorageError):
    """
    Raised when a required file cannot be read.
    """
    pass


class StorageSpaceError(StorageError):
    """
    Raised when there is insufficient disk space.
    """
    pass


class StoragePermissionError(StorageError):
    """
    Raised when the application does not have permission to access the storage location.
    """
    pass