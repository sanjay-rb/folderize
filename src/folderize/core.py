import argparse
import os
import logging
import re
import yaml
import sys
from pathlib import Path
from .exceptions import (
    FolderizeError,
    StructureFileNotFound,
    InvalidDefineFormat,
    YamlParseError,
    PlaceholderNotFound,
    FolderCreationError,
)

logger = logging.getLogger(__name__)


def setup_logging(verbose=False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def setup_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Folderize: Generate folder structures from YAML definitions."
    )
    parser.add_argument("file", nargs="?", help="Path to YAML structure file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    parser.add_argument(
        "-D",
        "--define",
        nargs="*",
        default=[],
        metavar="KEY=VALUE",
        help="Template variables (KEY=VALUE)",
    )
    return parser


def replace_placeholders(text, variables) -> str:
    def repl(match):
        key = match.group(1)
        if key in variables:
            return variables[key]
        raise PlaceholderNotFound(key)

    return re.sub(r"<(\w+)>", repl, text)


def create_from_yaml(d, base_path="") -> None:
    """Recursively creates folders and files from nested dict."""
    for name, content in d.items():
        path = os.path.join(base_path, name)
        try:
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                create_from_yaml(content, path)
            else:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w") as f:
                    f.write(str(content))
                logger.debug(f"Created file: {path}")
        except OSError as e:
            raise FolderCreationError(path, str(e))


def main() -> int:
    parser = setup_argparse()
    args = parser.parse_args()

    setup_logging(args.verbose)

    # Default file
    if not args.file:
        args.file = "STRUCTURE.yaml"
        logger.info(f"No file specified. Using default: {args.file}")

    # Parse variables
    variables = {}
    for pair in args.define:
        if "=" not in pair:
            raise InvalidDefineFormat(pair)
        key, value = pair.split("=", 1)
        variables[key] = value

    # Read & parse YAML
    filepath = Path(args.file)
    if not filepath.exists():
        raise StructureFileNotFound(args.file)

    try:
        with open(filepath) as f:
            yaml_text = f.read()
            if variables:
                yaml_text = replace_placeholders(yaml_text, variables)
            structure = yaml.safe_load(yaml_text)
            if structure is None:
                raise YamlParseError(args.file, "Empty or invalid YAML")
    except yaml.YAMLError as e:
        raise YamlParseError(args.file, str(e))

    # Create structure
    try:
        create_from_yaml(structure)
        logger.info("Folder structure created successfully!")
        return 0
    except FolderCreationError:
        raise  # Re-raise for main() to catch
