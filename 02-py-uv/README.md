# What is the UV?

**UV**  is a modern, high-performance Python package manage

## Features

- Lightning-fast package installation and dependency resolution
- Compatible with existing Python tools and workflows
- Built-in virtual environment management
- Support for modern packaging standards
- Reliable dependency locking and reproducible environments
- Memory-efficient operation, especially for large projects

---

## Method 1: Create UV Project Using a Package

### Step 1: Install UV (create environment Automatic)

```bash
pip install uv
```

```bash
uv init --package example-pkg
```

```bash
uv run example-pkg

```


## Method 2: Create UV Project Using a Package

```bash
uv init test
```

**download library external**

```bash
uv add openai-agents
```

**run project**
```bash
uv run uv run main.py
```

| Command                         | Action                                                              |
| ------------------------------- | ------------------------------------------------------------------- |
| `uv init --package example-pkg` | Creates a project and installs the `example-pkg` Python package.    |
| `uv init example-pkg`           | Creates a folder/project named `example-pkg`, no package installed. |

