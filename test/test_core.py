import sys

import pytest

from folderize.core import create_from_yaml, main, replace_placeholders
from folderize.exceptions import (
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


def test_main_uses_default_structure_file(monkeypatch, tmp_path):
    structure_file = tmp_path / "STRUCTURE.yaml"
    structure_file.write_text('app:\n  main.py: ""\n')

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["folderize"])

    exit_code = main()

    assert exit_code == 0
    assert (tmp_path / "app" / "main.py").exists()


def test_main_raises_when_structure_file_missing(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["folderize", "does-not-exist.yaml"])

    with pytest.raises(StructureFileNotFound):
        main()


def test_main_raises_for_invalid_define_format(monkeypatch, tmp_path):
    structure_file = tmp_path / "structure.yaml"
    structure_file.write_text("root: {}\n")

    monkeypatch.setattr(
        sys,
        "argv",
        ["folderize", str(structure_file), "-D", "missing_equals"],
    )

    with pytest.raises(InvalidDefineFormat):
        main()


def test_main_raises_yaml_parse_error(monkeypatch, tmp_path):
    structure_file = tmp_path / "bad.yaml"
    structure_file.write_text("foo: [bar\n")

    monkeypatch.setattr(sys, "argv", ["folderize", str(structure_file)])

    with pytest.raises(YamlParseError):
        main()


def test_main_raises_placeholder_not_found(monkeypatch, tmp_path):
    structure_file = tmp_path / "structure.yaml"
    structure_file.write_text('<project>:\n  README.md: ""\n')

    monkeypatch.setattr(
        sys,
        "argv",
        ["folderize", str(structure_file), "-D", "unused=value"],
    )

    with pytest.raises(PlaceholderNotFound):
        main()


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
