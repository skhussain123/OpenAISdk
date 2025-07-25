

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
print(result.final_output) 
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


## Session kya hai?

* Session asal mein aik aisa tasawwur hai jis ki madad se har fard ya guftagu ke liye alag se chat history rakhi jati hai, takay har session mein usi makhsoos guftagu ka record ho.
* Session implementations ke liye ek Protocol muhaiya kiya gaya hai.
* Session khud ba khud ya aap ki hidayat par messages shamil, hazf ya saaf kar sakta hai.

### Important Functions

| **Function**    | **Purpose**                                                                   |
| --------------- | ----------------------------------------------------------------------------- |
| `get_items`     | To read the complete or limited conversation history (e.g., last 10 messages) |
| `add_items`     | To add new messages to the conversation history                               |
| `pop_item`      | To remove and return the most recent (last) message from the session history  |
| `clear_session` | To completely delete the entire conversation history                          |


### SQLiteSession

* SQLiteSession is module ki default implementation hai. Yeh session data ko SQLite database mein mehfooz karti hai.
* In-Memory: Agar aap database ka raasta na dein to yeh sari history arzi tor par yaad-dasht (memory) mein rakhta hai jo program band hotay hi khatam ho jati hai.
* Persistent Storage: Aur agar raasta dein to file mein mustaqil tor par record rakhta hai.


### properties aur functions:

* __init__: Session bananay ka function jismein session ID, database ka raasta aur tables ke naam set kiye ja sakte hain.
* get_items: Session ki puri ya jukhti history wapas lata hai.
* add_items: Nai entries ko SQLite mein save karta hai.
* pop_item: Aakhri message ko nikaal kar deta hai.
* clear_session: Is session ki puri data history delete kar deta hai.
* close: Database connection band kar deta hai.


### Session ka Use Case
* Har user ya guftagu ke liye alag session/ID honi chahiye.
* Waqti chat ke liye in-memory SQLite behtareen hai jabke mehfooz guftagu ke liye file-wala SQLite istemal karein.
* Ek hi database mein kai mukhtalif guftaguon ki history rakhne ki sahulat mojood hai.
* Apni zarurat ke mutabiq agar chahen to custom backend (jaise Redis, Postgres) bhi implement kar sakte hain, bas woh Session Protocol ke mutabiq ho.

OpenAI Agents SDK ka Memory module, khaas tor par SQLiteSession, stateful conversations aur chat apps ke liye kaafi aasan aur mazboot hal muhaiya karta hai, jis se agents ko har user ki guftagu yaad rakhne, retrieve karne aur clear karne ki mukammal sahulat milti hai.


https://openai.github.io/openai-agents-python/sessions/
https://openai.github.io/openai-agents-python/ref/memory/
