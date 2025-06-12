
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
uv add chainlit
```

### 3. Add openai-agents
```bash 
uv add openai-agents
```

### 4. Run project
```bash 
uv run chainlit run hello.py -w --port 8500
```

### Documentation

Chainlit library ko import karta hai. Yeh chatbot ke UI aur lifecycle ko control karta hai (like on start, on message, etc).
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

```bash
from agents.run import RunConfig
from openai.types.responses import ResponseTextDeltaEvent
```
* RunConfig: Agent ka configuration (model, provider, tracing etc.).
* ResponseTextDeltaEvent: Streaming response ko handle karne ke liye specific event type.


.env file se GEMINI_API_KEY load karta hai jo Google Gemini API ka key hai.
```bash
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
```

**Model and Agent Setup**
Gemini ko OpenAI-compatible wrapper ke through access karne ke liye client banaya gaya hai.
```bash
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
```

Model specify kiya gaya hai: "gemini-2.0-flash" using the wrapped provider.
```bash
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)
```

Agent ke run hone ka configuration: model, provider, and tracing off.
```bash
config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)
```

Ek agent banaya gaya hai jiska naam hussain hai. Instructions diya gaya hai ki "best possible answer do"
```bash
agent1 = Agent(
    instructions="Answer the question as best you can.",
    name="hussain",
)
```

**Message Handler**
Har message ke liye yeh function trigger hota hai.
```bash
@cl.on_message
async def on_message(message: cl.Message):
```

* Pehle se existing conversation history li jati hai.
* Ek empty message placeholder banaya jata hai (jisme later token stream hoga).

```bash
history = cl.user_session.get("history", [])
msg = cl.Message(content="")
await msg.send()
```

User ka message history me add kiya jata hai.
```bash
history.append({"role": "user", "content": message.content})
```

**Run Agent and Stream Response**
Agent agent1 run hota hai with the user's input using run_streamed.
```bash
    result = Runner.run_streamed(
        agent1,
        input=message.content,
        run_config=config,
    )
```


* Real-time stream ke through agent ka har token (word/phrase) receive hota hai aur UI me dikhaya jata hai.
* Yeh live typing effect create karta hai.
```bash
async for event in result.stream_events():
    if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
        token = event.data.delta
        await msg.stream_token(token)
```

**Update History and Error Handling**
Final assistant response ko history me save kiya jata hai.
```bash
history.append({"role": "assistant", "content": result.final_output})
cl.user_session.set("history", history)
```

Agar koi error aata hai to use console me print kiya jata hai aur user ko notify kiya jata hai.
```bash
except Exception as e:
    print(e)
    await msg.send("Error: " + str(e))
```