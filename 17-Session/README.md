

## Sessions
The Agents SDK provides built-in session memory to automatically maintain conversation history across multiple agent runs, eliminating the need to manually handle .to_input_list() between turns.

Sessions stores conversation history for a specific session, allowing agents to maintain context without requiring explicit manual memory management. This is particularly useful for building chat applications or multi-turn conversations where you want the agent to remember previous interactions.

### Quick start
```bash
from agents import Agent, Runner, SQLiteSession

# Create agent
agent = Agent(
    name="Assistant",
    instructions="Reply very concisely.",
)

# Create a session instance with a session ID
session = SQLiteSession("conversation_123")

# First turn
result = await Runner.run(
    agent,
    "What city is the Golden Gate Bridge in?",
    session=session
)
print(result.final_output)  # "San Francisco"

# Second turn - agent automatically remembers previous context
result = await Runner.run(
    agent,
    "What state is it in?",
    session=session
)
print(result.final_output)  # "California"

# Also works with synchronous runner
result = Runner.run_sync(
    agent,
    "What's the population?",
    session=session
)
print(result.final_output)  # "Approximately 39 million"
```








### Code Example
```bash
import os
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import (
    Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,
    RunConfig, set_tracing_disabled, SQLiteSession
)
from agents.run import RunContextWrapper

# Load env variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

# Tracing disable
set_tracing_disabled(disabled=True)

# store chat history this file 
chat_log_path = "chat_history.txt"

# Main async function
async def main():
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-1.5-flash",
        openai_client=external_client
    )

    config = RunConfig(
        model=model,
        model_provider=external_client
    )

    main_agent = Agent(
        name="Helpful Assistant",
        instructions="You are a helpful assistant. Use tools when needed. If user asks a math question, call the Math Assistant.",
        model=model,
    )

    session = SQLiteSession("my_convo_001")

    print("Chatbot is ready. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ['exit', 'quit']:
            print("Exiting chat.")
            break

        try:
            result = await Runner.run(
                main_agent,
                user_input,
                run_config=config,
                session=session
            )

            # Print assistant response
            print("Assistant:", result.final_output)

            # Save chat history to file
            with open(chat_log_path, "a", encoding="utf-8") as f:
                f.write(f"You: {user_input}\n")
                f.write(f"Assistant: {result.final_output}\n\n")

        except Exception as e:
            print(f"[ERROR] {e}")

# Start program
if __name__ == "__main__":
    asyncio.run(main())
```

#### How it works
##### When session memory is enabled:

* Before each run: The runner automatically retrieves the conversation history for the session and prepends it to the input items.
* After each run: All new items generated during the run (user input, assistant responses, tool calls, etc.) are automatically stored in the session.
* Context preservation: Each subsequent run with the same session includes the full conversation history, allowing the agent to maintain context.

This eliminates the need to manually call .to_input_list() and manage conversation state between runs.

### Memory operations
#### Basic operations

##### 1. Sessions supports several operations for managing conversation history:
```bash
session = SQLiteSession("user_123", "conversations.db")
```

##### 2. Get all items in a session
```bash
items = await session.get_items()
```

##### 3. New Items Add Karna
```bash
new_items = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"}
]
await session.add_items(new_items)
```

##### 4. Aakhri Message Remove Karna
```bash
last_item = await session.pop_item()
print(last_item)
```

##### 5. Pure Session Ko Clear Karna
```bash
await session.clear_session()
```

#### No memory (default)
```bash
# Default behavior - no session memory
result = await Runner.run(agent, "Hello")
```

### Multiple sessions
```bash
from agents import Agent, Runner, SQLiteSession

agent = Agent(name="Assistant")

# Different sessions maintain separate conversation histories
session_1 = SQLiteSession("user_123", "conversations.db")
session_2 = SQLiteSession("user_456", "conversations.db")

result1 = await Runner.run(
    agent,
    "Hello",
    session=session_1
)
result2 = await Runner.run(
    agent,
    "Hello",
    session=session_2
)
```
