import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from openai.types.responses import ResponseTextDeltaEvent

# Load environment variables
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

agent1 = Agent(
    instructions="Answer the question as best you can.",
    name="hussain",
)

async def main():
    try:
        result = Runner.run_streamed(
            agent1,
            input="How AI is Changing the World in 2025",
            run_config=config,
        )

        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta)

    except Exception as e:
        print("Error:", str(e))

asyncio.run(main())
