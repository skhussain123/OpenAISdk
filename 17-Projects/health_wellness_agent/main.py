# main.py

import asyncio
import os
from dotenv import load_dotenv
import sys

from agents import Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from openai.types.responses import ResponseTextDeltaEvent
from context import UserSessionContext
from hooks import LoggingRunHooks

from agent import SeparateAgent 

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# OpenAI setup
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,
)

history = []  # Global history list


# Async runner
async def main():
    hooks = LoggingRunHooks()

    while True:
        query = input("💬 Enter your health/wellness query (or type 'exit' to quit): ")

        if query.lower() == "exit":
            print("👋 Goodbye!")
            break

        history.append({"role": "user", "content": query})

        # Create agent instance from agent.py
        agent_instance = SeparateAgent(history, query)

        try:
            result = Runner.run_streamed(
                agent_instance.triage_agent,
                input=query,
                run_config=config,
                context=UserSessionContext(name="TestUser", uid=12345),
                hooks=hooks,
            )

            full_response = ""
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    full_response += event.data.delta

            try:
                from json import loads
                data = loads(full_response)
                final_message = data.get("response", "")
            except:
                final_message = full_response.strip()

            print(final_message)
            history.append({"role": "assistant", "content": final_message})

        except Exception as e:
            print(f"❌ Error: {str(e)}")


# Entry point
if __name__ == "__main__":
    asyncio.run(main())
