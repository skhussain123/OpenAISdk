import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, handoff, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load API Key
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Setup Gemini OpenAI-compatible Client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Model setup
model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=external_client
)

# Runner config
config = RunConfig(
    model=model,
    model_provider=external_client,
)

# Urdu agent
urdu_agent = Agent(
    name="Urdu Agent",
    instructions="آپ صرف اردو میں جواب دیتے ہیں۔"
)

# English agent
english_agent = Agent(
    name="English Agent",
    instructions="You only respond in English."
)

# Triage agent with handoff logic
triage_agent = Agent(
    name="Triage Agent",
    instructions="""
If the input is in Urdu or contains Urdu characters, then handoff to the Urdu Agent.
Otherwise, handoff to the English Agent.
""",
    handoffs=[handoff(urdu_agent), handoff(english_agent)],
)

# Runner
async def main(input: str):
    result = await Runner.run(triage_agent, input=input, run_config=config)
    print("\n🧠 Final Output:\n", result.final_output)

# Example Run
asyncio.run(main(input("Enter Your Query")))
