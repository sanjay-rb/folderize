class FolderizeError(Exception):
    """Base exception for all folderize errors."""


class StructureFileNotFound(FolderizeError):
    """Raised when the structure YAML file is missing."""

    def __init__(self, filepath):
        super().__init__(f"Structure file '{filepath}' not found.")


class InvalidDefineFormat(FolderizeError):
    """Raised when -D key=value format is invalid."""

    def __init__(self, pair):
        super().__init__(
            f"Invalid -D/--define format '{pair}'. Use: folderize -D key=value."
        )


class YamlParseError(FolderizeError):
    """Raised when YAML parsing fails."""

    def __init__(self, filepath, error):
        super().__init__(f"YAML parse error in '{filepath}': {error}")


class PlaceholderNotFound(FolderizeError):
    """Raised when a placeholder <KEY> has no value."""

    def __init__(self, key):
        super().__init__(
            f"Placeholder <{key}> not provided. Use: folderize -D {key}=value"
        )


class FolderCreationError(FolderizeError):
    """Raised when directory/file creation fails."""

    def __init__(self, path, error):
        super().__init__(f"Failed to create '{path}': {error}")
