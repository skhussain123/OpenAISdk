import os
import asyncio
from dataclasses import dataclass
from dotenv import load_dotenv

from agents import Agent, Runner, RunContextWrapper, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig
from context import UserSessionContext

# Load environment variables (optional, in case you want to move the API key to .env file)
load_dotenv()
# Define a function tool that uses the context
# Gemini API Key (either use .env or hardcode here)
gemini_api_key = 'AIzaSyCnkIzE4fdmJxLOJdRdPGo3s_ZMSzC5L3o'

# Validate key
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set!")

# Setup Gemini OpenAI-compatible client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Setup Gemini Model
model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash", 
    openai_client=external_client
)

# RunConfig with model and provider
config = RunConfig(
    model=model,
    model_provider=external_client
)


# Agent that uses the context-aware tool
agent = Agent(
    name="Assistant",
    model=model
)

# Main runner
async def main():
    # Run the agent
    result = await Runner.run(
        starting_agent=agent,
        input="What is the age of the user?",
        context=UserSessionContext(name="TestUser", uid=12345),
        run_config=config
    )

    print("\n Final Output:\n", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
