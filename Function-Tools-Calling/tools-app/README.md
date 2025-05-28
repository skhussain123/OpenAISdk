

# Function And Tool Calling

uv add openai-agents
uv add python-dotenv

#### Create a Custom pytho Function using function_tool
```bash
@function_tool
def get_live_weather(location: str) -> str:
    """
    Returns the current weather for a given location.
    For now, returns a static message to test if the function is being called.
    """
    return f"Static response: Weather function called for location: {location}"\


```
#### Register Function in Agent
```bash
agent: Agent = Agent(
    name="Assistant", 
    instructions="You are a helpful assistant", 
    model=model,
    tools=[get_live_weather],  # Registering the tool
    
    )
```
