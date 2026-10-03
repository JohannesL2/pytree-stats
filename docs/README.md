# pytree-stats

![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

<p align="center">

<img width="128" height="128" src="https://github.com/user-attachments/assets/4b45c09f-1aa2-4277-a760-94b916b9e829" alt="pytree-stats logo" />

</p>

A fast, lightweight Python command-line utility for generating directory tree listings with statistics. Use it to inspect folder hierarchies, share structured snapshots with LLMs (ChatGPT/Claude), or document project layouts.

<p align="center">

<img alt="pytree-stats screenshot" src="https://github.com/user-attachments/assets/afccc1ae-e935-4f32-ae22-1fe169294009" width="500" />

</p>

## Features

- **Global CLI Utility:** Run `pytree` from any directory in your terminal.
- **AI & LLM Friendly:** Generates structured output easy for LLMs to parse and understand.
- **Smart Ignore Defaults:** Automatically skips common noise directories like `.git`, `node_modules`, `.venv`, and `__pycache__`.
- **Custom Filtering:** Pass your own ignore rules via `-i` / `--ignore`.
- **Export Capabilities:** Instantly copy results to clipboard or export directly to a Markdown file.
- **Rich Terminal Output:** Colored syntax and clean directory stats powered by [Rich](https://github.com/Textualize/rich).

---

## Installation & Setup

### Prerequisites

- Python 3.8+

### Install as a System-Wide CLI

1. Clone the repository:

```bash
git clone https://github.com/JohannesL2/pytree-stats.git
cd pytree-stats
```

Install locally in editable mode:

```bash
pip install -e .
```

Now you can use the pytree command from any directory on your computer!

## Usage

```bash
# Scan the current working directory
pytree

# Scan a specific directory
pytree /path/to/project

# Ignore custom subdirectories (comma-separated)
pytree -i "dist,build,custom_folder"

# Export the output directly to a Markdown file
pytree --markdown output.md
```

## Contributing

Contributions are welcome and greatly appreciated!

### Fork & Clone

```bash
git clone https://github.com/JohannesL2/pytree-stats.git
cd pytree-stats
```

### Set up a Virtual Environment & Dev Dependencies

```bash
python3 -m venv venv
source venv/bin/activate # On Windows: venv\\Scripts\\activate
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Open a Pull Request

Create a new branch for your feature or bugfix and submit a PR!

Check out open issues labeled good first issue to get started.

## License

This project is licensed under the MIT License.