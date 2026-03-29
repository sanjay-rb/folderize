import sys

import pytest

from folderize.core import create_from_yaml, main, replace_placeholders
from folderize.exceptions import (
    FolderCreationError,
    InvalidDefineFormat,
    PlaceholderNotFound,
    StructureFileNotFound,
    YamlParseError,
)


def test_replace_placeholders_success():
    text = "name: <project>"

    assert replace_placeholders(text, {"project": "demo"}) == "name: demo"


def test_replace_placeholders_missing_key_raises():
    with pytest.raises(PlaceholderNotFound):
        replace_placeholders("name: <project>", {})


def test_create_from_yaml_creates_nested_files(tmp_path):
    structure = {
        "src": {
            "main.py": "print('hello')",
            "pkg": {"__init__.py": ""},
        },
        "README.md": "# Demo",
    }

    create_from_yaml(structure, str(tmp_path))

    assert (tmp_path / "src" / "main.py").read_text() == "print('hello')"
    assert (tmp_path / "src" / "pkg" / "__init__.py").exists()
    assert (tmp_path / "README.md").read_text() == "# Demo"


def test_create_from_yaml_top_level_file(tmp_path):
    """Regression test: top-level files must not fail due to empty dirname."""
    structure = {"README.md": "# Hello"}

    create_from_yaml(structure, str(tmp_path))

    assert (tmp_path / "README.md").read_text() == "# Hello"


def test_create_from_yaml_rejects_absolute_path(tmp_path):
    structure = {"/etc/passwd": "bad"}
    with pytest.raises(FolderCreationError):
        create_from_yaml(structure, str(tmp_path))


def test_create_from_yaml_rejects_path_traversal(tmp_path):
    structure = {"../escape": "bad"}
    with pytest.raises(FolderCreationError):
        create_from_yaml(structure, str(tmp_path))


def test_main_uses_default_structure_file(monkeypatch, tmp_path):
    structure_file = tmp_path / "STRUCTURE.yaml"
    structure_file.write_text('app:\n  main.py: ""\n')

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["folderize"])

    exit_code = main()

    assert exit_code == 0
    assert (tmp_path / "app" / "main.py").exists()


def test_main_returns_error_when_structure_file_missing(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["folderize", "does-not-exist.yaml"])

    assert main() == 1


def test_main_returns_error_for_invalid_define_format(monkeypatch, tmp_path):
    structure_file = tmp_path / "structure.yaml"
    structure_file.write_text("root: {}\n")

    monkeypatch.setattr(
        sys,
        "argv",
        ["folderize", str(structure_file), "-D", "missing_equals"],
    )

    assert main() == 1


def test_main_returns_error_for_yaml_parse_error(monkeypatch, tmp_path):
    structure_file = tmp_path / "bad.yaml"
    structure_file.write_text("foo: [bar\n")

    monkeypatch.setattr(sys, "argv", ["folderize", str(structure_file)])

    assert main() == 1


def test_main_returns_error_when_placeholder_not_found(monkeypatch, tmp_path):
    structure_file = tmp_path / "structure.yaml"
    structure_file.write_text('<project>:\n  README.md: ""\n')

    monkeypatch.setattr(
        sys,
        "argv",
        ["folderize", str(structure_file), "-D", "unused=value"],
    )

    assert main() == 1


def test_main_returns_error_when_placeholder_and_no_defines(monkeypatch, tmp_path):
    """Placeholders in YAML without any -D flag must return error code 1."""
    structure_file = tmp_path / "structure.yaml"
    structure_file.write_text('<project>:\n  README.md: ""\n')

    monkeypatch.setattr(sys, "argv", ["folderize", str(structure_file)])

    assert main() == 1


def test_main_success_with_define(monkeypatch, tmp_path):
    structure_file = tmp_path / "structure.yaml"
    structure_file.write_text("<project>:\n  app.py: \"print('ok')\"\n")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        "argv",
        ["folderize", str(structure_file), "-D", "project=my_app"],
    )

    exit_code = main()

    assert exit_code == 0
    assert (tmp_path / "my_app" / "app.py").read_text() == "print('ok')"


def test_main_returns_error_for_non_dict_yaml(monkeypatch, tmp_path):
    """YAML root that is not a mapping must return error code 1."""
    structure_file = tmp_path / "list.yaml"
    structure_file.write_text("- item1\n- item2\n")

    monkeypatch.setattr(sys, "argv", ["folderize", str(structure_file)])

    assert main() == 1

