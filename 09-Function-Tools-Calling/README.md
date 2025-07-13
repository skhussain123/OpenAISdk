


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
