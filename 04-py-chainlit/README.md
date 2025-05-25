# What is the Chainlit?

**UV** is a high-performance Python web framework or server designed for speed and simplicity. It's ideal for building fast APIs or web apps with minimal setup. Inspired by event-driven frameworks like Node.js and Uvicorn, UV allows you to build modern async applications in Python with ease.

## Features

- Fast and lightweight
- Asynchronous by design
- Minimal setup required
- Inspired by modern web frameworks

## Install the package using pip:

```bash
pip install uv
```

```bash
uv init hello_chainlit
```


```bash
uv add chainlit 
```


```bash
uv run chainlit hello
```
**create environment Automatic**


```bash
uv run chainlit run chatbot.py -w
```


#### create chatbot.py file in root directory and use this code 

```bash
import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    # Our custom logic goes here...
    # Send a fake response back to the user
    await cl.Message(
        content=f"Received: {message.content}",
    ).send()
```

**then run project**

```bash
uv run chainlit run chatbot.py -w
```

**or**

```bash
uv run chainlit run chatbot.py -w --port 8500
``` 