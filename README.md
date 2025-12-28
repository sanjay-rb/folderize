# Folderize

**Folderize** is a Python command-line tool that generates a directory structure from definitions provided in a `STRUCTURE.md` file. It helps developers quickly scaffold projects in a consistent and repeatable way.

---

## ✨ Features

* 📁 Automatically creates folders based on a simple markdown structure
* ⚡ Fast and easy to use via a CLI command
* 🧩 Ideal for project scaffolding and standardizing directory layouts
* 📝 Uses a human-readable `STRUCTURE.md` file as input

---

## 📦 Installation

Install Folderize using pip:

```bash
pip install folderize
```

---

## 🚀 Usage

Create a `STRUCTURE.md` file describing your desired folder layout.

Example `STRUCTURE.md`:

```text
src/
  components/
  utils/
tests/
docs/
```

Run Folderize from the command line:

```bash
folderize STRUCTURE.md
```

Folderize will generate the corresponding directory structure in the current working directory.

---

## 🛠 How It Works

Folderize reads the structure defined in the `STRUCTURE.md` file and creates directories that match the specified hierarchy. It focuses on simplicity, allowing you to define folder layouts without complex configuration files.

---

## 🎯 Use Cases

* Bootstrapping new projects
* Enforcing consistent folder structures across teams
* Quickly recreating directory layouts
* Learning or teaching project organization best practices

---

## 📄 Requirements

* Python 3.7 or higher

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve Folderize.

---

## 📜 License

This project is licensed under the MIT License.

---

### Optional `pyproject.toml` snippet

Make sure PyPI renders this correctly:

```toml
[project]
readme = "README.md"
```