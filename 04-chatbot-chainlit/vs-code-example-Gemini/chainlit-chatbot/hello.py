import chainlit as cl
import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from openai.types.responses import ResponseTextDeltaEvent

# Load environment variables
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

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
    tracing_disabled=True
)

agent1 = Agent(
    instructions="Answer the question as best you can.",
    name="hussain",
)

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content="Hello! I am your assistant. How can I help you today?").send()

@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get("history", [])
    msg = cl.Message(content="")
    await msg.send()

    history.append({"role": "user", "content": message.content})

    try:
        result = Runner.run_streamed(
            agent1,
            input=message.content,
            run_config=config,
        )

        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                token = event.data.delta
                await msg.stream_token(token)

        history.append({"role": "assistant", "content": result.final_output})
        cl.user_session.set("history", history)

    except Exception as e:
        print(e)
        await msg.send("Error: " + str(e))

