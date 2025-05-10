
# 🚀 Chainlit Chatbot with OpenAI Agents

A simple Chainlit-based chatbot project using `openai-agents`.

---

## 📁 Project Setup

### 1. Create a New Project
```bash
uv init chainlit-chatbot

```

```bash 
cd chainlit-chatbot
```

### 2. Add chainlit
```bash 
cd add chainlit
```

### 3. Add openai-agents
```bash 
uv add openai-agents
```

### 4. Run project
```bash 
uv run chainlit run hello.py -w --port 8500
```

Documentation

# Chainlit library ko import karta hai. Yeh chatbot ke UI aur lifecycle ko control karta hai (like on start, on message, etc).
```bash
import chainlit as cl 
```

```bash
import os
from dotenv import load_dotenv
```
* os module environment variables access karne ke liye.
* load_dotenv() .env file se environment variables ko load karta hai (jaise API keys).


```bash
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
```
* agents library ke components import kar raha hai:
  * Agent: Aapka AI assistant object.
  * Runner: Agent ko run karne ke liye.
  * AsyncOpenAI: Asynchronous API handler.
  * OpenAIChatCompletionsModel: Model configuration (yahan Gemini use ho raha hai OpenAI wrapper ke through).



