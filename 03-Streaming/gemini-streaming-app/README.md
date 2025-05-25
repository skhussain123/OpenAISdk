# Gemini Streaming App (Gemini-2.0 Flash)

This project demonstrates how to interact with the **Google Gemini API** using a streaming response interface inspired by OpenAI-style agents.

---

## 🚀 Features

- Uses the `gemini-2.0-flash` model with streaming support.
- Streams AI-generated content token by token.
- Async-based architecture.
- Easy to plug into chat interfaces or content generators.

---

## 🛠️ Tech Stack

- Python 3.10+
- `dotenv` for environment variable management
- `asyncio` for asynchronous code execution
- `agents` SDK for structured AI agent setup
- Google Gemini API (`generativelanguage.googleapis.com`)

---

## 📷 Demo

![Streaming Demo](assets/demo.png)

---

## 📦 Installation & Environment Setup

1. **Initialize the project using `uv`:**

```bash
uv init gemini-streaming-app
cd gemini-streaming-app

```

2. **Install required packages:**
```bash
uv add openai-agents python-dotenv
```


3. **Creare Api using Google Ai Studio:**
https://aistudio.google.com/prompts/new_chat


