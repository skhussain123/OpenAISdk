import os
import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY") 
MODEL = "openai/gpt-3.5-turbo"

client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

async def main():
    agent = Agent(
    name="Assistant",
    model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
    )

    result = await Runner.run(
        agent,
        "Write a detailed 500-word blog discussing the impact of artificial intelligence (AI) on jobs in 2025",
    )
    
    print('Response Start------------------------------------------------------')
    print(result.final_output)
    print('Response End------------------------------------------------------')
    
asyncio.run(main())
    
    
    
