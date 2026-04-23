# pytree-stats

https://img.shields.io/badge/PRs-welcome-brightgreen.svg

A small Python command-line utility for generating directory tree listings. Use it to inspect folder hierarchies, share file structure snapshots, or compare directory layouts across projects.

<img alt="screenshot" src="https://github.com/user-attachments/assets/afccc1ae-e935-4f32-ae22-1fe169294009" width="400" alt="pytree-stats screenshot" />

## What the project does

`pytree-stats` reads a filesystem path and prints a tree-style view of the directory contents. It is designed as a lightweight, easy-to-run Python script that works without complex setup.

## Why the project is useful

- Quickly inspect folder structure from the terminal
- **AI-Friendly:** Generates structured output that is easy for LLMs to parse.
- Useful for documentation, code reviews, and project audits
- Works cross-platform with Python
- Simple, no heavy dependencies

## Get started

### Prerequisites

- Python 3.7+
- [Rich](https://github.com/Textualize/rich) library
- [pyperclip](https://github.com/asweigart/pyperclip) library

### Installation

1. Clone the repository:

```bash
git clone https://github.com/JohannesL2/pytree-stats.git
cd pytree-stats
```

2. Install dependencies:

```bash
pip install rich
pip install pyperclip
```

3. Run the script

```bash
python tree.py
```
