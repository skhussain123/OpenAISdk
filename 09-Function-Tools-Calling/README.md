


## Tools
Tools let agents take actions: things like fetching data, running code, calling external APIs, and even using a computer. There are three classes of tools in the Agent SDK:


### 1. Hosted tools:
Hosted tools are tools that are managed and run by OpenAI or third-party providers, so you don’t need to build, deploy, or manage them yourself. You just declare them in your assistant or agent configuration, and they work out of the box.

### 2. Function calling:
Function calling allows the AI to call your custom functions with structured inputs and use the returned results in its responses.

### 3. Agents as tools:
“Agents as tools” means you can use one AI agent inside another agent, just like you use a normal tool or function.


## Hosted tools
* OpenAI offers a few built-in tools when using the OpenAIResponsesModel:

1. The WebSearchTool lets an agent search the web.
2. The FileSearchTool allows retrieving information from your OpenAI Vector Stores.
3. The ComputerTool allows automating computer use tasks.
4. The CodeInterpreterTool lets the LLM execute code in a sandboxed environment.
5. The HostedMCPTool exposes a remote MCP server's tools to the model.
6. The ImageGenerationTool generates images from a prompt.
7. The LocalShellTool runs shell commands on your machine.

```bash
from agents import Agent, FileSearchTool, Runner, WebSearchTool

agent = Agent(
    name="Assistant",
    tools=[
        WebSearchTool(),
        FileSearchTool(
            max_num_results=3,
            vector_store_ids=["VECTOR_STORE_ID"],
        ),
    ],
)

async def main():
    result = await Runner.run(agent, "Which coffee shop should I go to, taking into account my preferences and the weather today in SF?")
    print(result.final_output)
```    

## Function tools / Function calling
You can use any Python function as a tool. The Agents SDK will setup the tool automatically:

1. The name of the tool will be the name of the Python function (or you can provide a name)
2. Tool description will be taken from the docstring of the function (or you can provide a description)
3. The schema for the function inputs is automatically created from the function's arguments
4. Descriptions for each input are taken from the docstring of the function, unless disabled


## Custom function tools
Sometimes, you don't want to use a Python function as a tool. You can directly create a FunctionTool if you prefer. You'll need to provide:

* name
* description
* params_json_schema, which is the JSON schema for the arguments
* on_invoke_tool, which is an async function that receives the context and the arguments as a JSON string, and must return the tool output as a string.


1. LLM (Large Language Model) pehle user ki query ko analyze karta hai.
2. LLM decides: "Mujhe koi tool call karna chahiye ya khud answer dena chahiye?"
3. Agar LLM ko lagta hai ke tool call karna zaroori hai, to:
  * Woh tool ka naam aur
  * parameters in JSON format (tool_input) define karta hai (following params_json_schema).
4. Agent us tool ko Python function ke form mein call karta hai.
5. Tool response return karta hai (string, dict, etc).
6. LLM tool ke output ko read karta hai.
7. Fir LLM final answer generate karta hai and returns it to the user.


```bash
@function_tool
def javascript(topic: str) -> str:
    "Explains a JavaScript topic in simple terms."
    return f"You asked about JavaScript topic: {topic}. Here's a basic explanation..."


agent = Agent(
    name="You are helpful assistant",
    instructions=("You are a helpful assistant for programming."),
    model=model,
    tools=[javascript],
)
```

### on_invoke_tool
Jab agent kisi tool ko call karne wala hota hai, on_invoke_tool waise hi chalta hai jaise "interceptor" ya "middleman" — jise aap bol sako:
"Ruko! Pehle mujhe check karne do tum kya call kar rahe ho."


## Automatic argument and docstring parsing
As mentioned before, we automatically parse the function signature to extract the schema for the tool, and we parse the docstring to extract descriptions for the tool and for individual arguments. Some notes on that:

1. The signature parsing is done via the inspect module. We use type annotations to understand the types for the arguments, and dynamically build a Pydantic model to represent the overall schema. It supports most types, including Python primitives, Pydantic models, TypedDicts, and more.

2. We use griffe to parse docstrings. Supported docstring formats are google, sphinx and numpy. We attempt to automatically detect the docstring format, but this is best-effort and you can explicitly set it when calling function_tool. You can also disable docstring parsing by setting use_docstring_info to False.

```bash
@function_tool
def greet(name: str) -> str:
    """Greets a user by name.

    Args:
        name: The name of the person to greet.
    """
    return f"Hello, {name}!"
```

## Agents as tools
In some workflows, you may want a central agent to orchestrate a network of specialized agents, instead of handing off control. You can do this by modeling agents as tools.

```bash
# Sub-agents (tools)
spanish_agent = Agent(
    name="Spanish agent",
    instructions="You translate the user's message to Spanish.",
    model=model
)

as_spanish_agent_tool = spanish_agent.as_tool(
    tool_name="translate_to_spanish",
    tool_description="Translate the user's message to Spanish.",
)

french_agent = Agent(
    name="French agent",
    instructions="You translate the user's message to French.",
    model=model
)

as_french_agent_tool = french_agent.as_tool(
    tool_name="translate_to_french",
    tool_description="Translate the user's message to French.",
)

# Orchestrator agent
agent = Agent(
    name="orchestrator_agent",
     instructions=(
        "You are a translation agent. You use the tools given to you to translate. "
        "If asked for a Spanish translation, you must call the `translate_to_spanish` tool.\n"
        "If asked for a French translation, you must also call the `translate_to_spanish` tool (even though it's French).\n"
        "You do not perform translation yourself. You must always use tools.\n"
        "If asked for both, call the appropriate tools as needed."
    ),
    model=model,
    tools=[
        as_spanish_agent_tool,
        as_french_agent_tool,
    ]
)
```

