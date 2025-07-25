
Lifecycle hooks ek tarah ke functions/methods hote hain jo automatically agent ya tool ke kisi important stage pe trigger hote hain — jaise start hone se pehle, complete hone ke baad, ya kisi tool ko call karne se pehle/baad.

* Logging kar sakein (jaise: tool kis waqt chala)
* Debug kar sakein (kya agent ne handoff kiya)
* Custom logic daal sakein (e.g., before tool run, validate inputs)


### Types of Hooks:
| Hook Type    | Kya Control Karta Hai         | Use Case Example                      |
| ------------ | ----------------------------- | ------------------------------------- |
| `RunHooks`   | **Global** – sab agents/tools | Har agent ya tool ke start/end pe log |
| `AgentHooks` | **Specific agent** ke liye    | Sirf NutritionAgent ke tool log karo  |


### RunHooksBase
A class that receives callbacks on various lifecycle events in an agent run. Subclass and override the methods you need.
**Bases: Generic[TContext, TAgent]**

#### 1. on_agent_start
Called before the agent is invoked. Called each time the current agent changes.

```bash
on_agent_start(
    context: RunContextWrapper[TContext], agent: TAgent
) -> None
```

#### 2. on_agent_end 
Called when the agent produces a final output.

```bash
on_agent_end(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    output: Any,
) -> None
```

#### 3. on_handoff
Called when a handoff occurs.

```bash
on_handoff(
    context: RunContextWrapper[TContext],
    from_agent: TAgent,
    to_agent: TAgent,
) -> None
```

#### 4. on_tool_end
Called after a tool is invoked.

```bash
on_tool_end(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    tool: Tool,
    result: str,
) -> None
```

### AgentHooksBase
**Bases: Generic[TContext, TAgent]**

A class that receives callbacks on various lifecycle events for a specific agent. You can set this on agent.hooks to receive events for that specific agent.

#### 1. on_start 
Called before the agent is invoked. Called each time the running agent is changed to this agent.

```bash
on_start(
    context: RunContextWrapper[TContext], agent: TAgent
) -> None
```

#### 2. on_end
Called when the agent produces a final output.

```bash
on_end(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    output: Any,
) -> None
```

#### 3. on_handoff
Called when the agent is being handed off to. The source is the agent that is handing off to this agent.

```bash
on_handoff(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    source: TAgent,
) -> None
```

#### 4. on_tool_start
Called before a tool is invoked.

```bash
on_tool_start(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    tool: Tool,
) -> None
```

#### 5. on_tool_end 
Called after a tool is invoked.

```bash
on_tool_end(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    tool: Tool,
    result: str,
) -> None
```

## Code Example RunHooks
```bash
import os
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import (
    Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,
    RunConfig, RunHooks, set_tracing_disabled, function_tool
)
from agents.run import RunContextWrapper


# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

set_tracing_disabled(disabled=True)


# --- Define JavaScript Tool ---
@function_tool
def javascript(topic: str) -> str:
    """Explains a JavaScript topic in simple terms."""
    return f"You asked about JavaScript topic: {topic}. Here's a basic explanation..."



# --- Define Hooks ---
class LoggingRunHooks(RunHooks):
    async def on_agent_start(self, context: RunContextWrapper, agent: Agent):
        print(f"[HOOK] Agent starting: {agent.name}")

    async def on_agent_finish(self, context: RunContextWrapper, agent: Agent, output):
        print(f"[HOOK] Agent ended: {agent.name} with output: {output}")

    async def on_tool_end(self, context: RunContextWrapper, agent: Agent, tool, result):
        print(f"[HOOK] Tool ended: {tool.name} returned: {result}")

    async def on_handoff(self, context: RunContextWrapper, from_agent: Agent, to_agent: Agent):
        print(f"[HOOK] Handoff from {from_agent.name} to {to_agent.name}")

    async def on_error(self, context: RunContextWrapper, agent: Agent, error: Exception):
        print(f"[HOOK] Error in agent '{agent.name}': {error}")



async def main():
    # Model setup
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-1.5-flash",
        openai_client=external_client
    )

    config = RunConfig(
        model=model,
        model_provider=external_client
    )
    
    Mathagent = Agent(
        name="Math Assistant",
        instructions="You are a helpful Math assistant",
        model=model,
    )

    # Agent setup with JavaScript tool
    triggle_agent = Agent(
        name="Helpful Assistant",
        instructions="You are a helpful assistant. Use tools when needed. if user ask math query then  Mathagent agent call",
        model=model,
        tools=[javascript],
        handoffs=[Mathagent]
    )

    # Hooks
    hooks = LoggingRunHooks()

    # Try with a JavaScript-related query
    query = "what is javascript"

    try:
        result = await Runner.run(triggle_agent, query, run_config=config, hooks=hooks)
        print("\n\nFinal Output:", result.final_output)

    except Exception as e:
        print(f"[HOOK] Error in agent '{triggle_agent.name}': {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Code Example Agent Hooks
```bash
import os
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import (
    Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,
    RunConfig, AgentHooks, set_tracing_disabled, function_tool
)
from agents.run import RunContextWrapper

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

set_tracing_disabled(disabled=True)


# --- Define JavaScript Tool ---
@function_tool
def javascript(topic: str) -> str:
    """Explains a JavaScript topic in simple terms."""
    return f"You asked about JavaScript topic: {topic}. Here's a basic explanation..."

class LoggingAgentHooks(AgentHooks):
    async def on_agent_start(self, context: RunContextWrapper, agent: Agent):
        print(f"[HOOK] Agent starting: {agent.name}")

    async def on_agent_end(self, context: RunContextWrapper, agent: Agent, output):
        print(f"[HOOK] Agent ended: {agent.name} with output: {output}")

    async def on_tool_use_start(self, context: RunContextWrapper, agent: Agent, tool, tool_input):
        print(f"[HOOK] Tool started: {tool.name} with input: {tool_input}")

    async def on_tool_use_end(self, context: RunContextWrapper, agent: Agent, tool, result):
        print(f"[HOOK] Tool ended: {tool.name} returned: {result}")

    async def on_handoff(self, context: RunContextWrapper, from_agent: Agent, to_agent: Agent):
        print(f"[HOOK] Handoff from {from_agent.name} to {to_agent.name}")

    async def on_error(self, context: RunContextWrapper, agent: Agent, error: Exception):
        print(f"[HOOK] Error in agent '{agent.name}': {error}")
        

# --- Main App ---
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

    # Math agent
    math_agent = Agent(
        name="Math Assistant",
        instructions="You are a helpful Math assistant",
        model=model
    )

    # Primary agent with tool + handoff
    main_agent = Agent(
        name="Helpful Assistant",
        instructions="You are a helpful assistant. Use tools when needed. If user asks a math question, call the Math Assistant.",
        model=model,
        tools=[javascript],
        handoffs=[math_agent]
    )

    hooks = LoggingAgentHooks()
    query = "what is 2+2" 

    try:
        result = await Runner.run(main_agent, query, run_config=config, hooks=hooks)
        print("\n\nFinal Output:", result.final_output)

    except Exception as e:
        print(f"[HOOK] Error in agent '{main_agent.name}': {e}")

if __name__ == "__main__":
    asyncio.run(main())

```