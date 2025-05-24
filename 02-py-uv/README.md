# What is the UV?

**UV** is a high-performance Python web framework or server designed for speed and simplicity. It's ideal for building fast APIs or web apps with minimal setup. Inspired by event-driven frameworks like Node.js and Uvicorn, UV allows you to build modern async applications in Python with ease.

## Features

- Fast and lightweight
- Asynchronous by design
- Minimal setup required
- Inspired by modern web frameworks

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

