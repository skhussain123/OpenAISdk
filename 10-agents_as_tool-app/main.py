import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

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
    model_provider=external_client,
)

# ✅ English Essay Agent
english_agent = Agent(
    name="English Essay Agent",
    instructions="Write a 3-paragraph essay in English on the user's topic.",
    model=model
)
english_tool = english_agent.as_tool(
    tool_name="english_essay_writer_tool",
    tool_description="Writes essays in English."
)

# ✅ Poetry Agent
poetry_agent = Agent(
    name="Poetry Writer Agent",
    instructions="Write a 3-stanza English poem on the given topic.",
    model=model
)
poetry_tool = poetry_agent.as_tool(
    tool_name="english_poetry_writer_tool",
    tool_description="Writes English poetry on the given topic."
)

# ✅ Triage Agent
triage_agent = Agent(
    name="Triage Agent",
    instructions="""
You are a smart assistant.
1. If the user asks for a poem or poetry, use 'english_poetry_writer_tool'.
2. Otherwise, use 'english_essay_writer_tool'.
Never write content yourself. Always call the right tool.
""",
    tools=[english_tool, poetry_tool],
    model=model
)

# === RUN ===
query = input("🟢 Enter your query (e.g., Write an essay or poem on pollution): ")

result = Runner.run_sync(
    triage_agent,
    query,
    run_config=config
)

print("\n📝 Response:\n", result.final_output)
