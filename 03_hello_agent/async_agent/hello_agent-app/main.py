import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import asyncio

# Load the environment
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is exists
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set.")


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)


async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are helpful Assistent.",
        model=model
    )

    result = await Runner.run(agent, "how to inspect ai health care.", run_config=config)
    print(result.final_output)
    

if __name__ == "__main__":
    asyncio.run(main())