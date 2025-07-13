
#### How to configure LLM Providers (Other than OpenAI) at different levels (Global, Run and Agent)?
* Agents SDK is setup to use OpenAI as default providers. When using other providers you can setup at different levels:

### 1. AGENT LEVEL
```bash
import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled

gemini_api_key = ""

#Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

set_tracing_disabled(disabled=True)

async def main():
    # This agent will use the custom LLM provider
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    )

    result = await Runner.run(
        agent,
        "Tell me about recursion in programming.",
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
```

#### Agent-Level Configuration 
Jab tum ek Agent banaatay ho, us waqt hi uska model, tools, aur instructions set kartay ho.

##### Socho Tum Ek Agent Bana Rahe Ho
```bash
agent = Agent(
    name="Hello Agent",
    instructions="Tumhara kaam hai user ko 'Hello' kehna.",
    model=model1  # GPT-4 ya koi bhi model
)

```
##### Ab Yeh Kya Hua?
1. Tumne agent ko bata diya ke woh kya kare (instructions)
2. Tumne agent ko ek model de diya (e.g. GPT-4)
3. Yeh sab uska "default setup" ban gaya — yani uska normal behavior


##### Jab Tum Agent Run Karte Ho Normally
```bash
Runner.run_sync(agent, "Say hello")
```

* Tumne Runner.run_sync() me kuch extra nahi diya (jaise run_config)
* Toh agent bolega: "Mere paas to already instructions aur model hain... wahi use kar leta hoon!"
* Yani agent ne apna default setup use kiya jo tumne uske start me diya tha.

##### Ab Socho Tum Chahtay Ho Temporary Change
```bash
from agents.run import RunConfig

config = RunConfig(
    model=model2  # ab GPT-3.5 use karo
)

Runner.run_sync(agent, "Say hello", run_config=config)
```
* Agent ne socha:"Aray mujhe to naye model ke sath chalaya gaya hai, chalo is bar model2 use karta hoon!"

* Is bar usne apna default setup nahi use kiya.
*  Usne run-level config use kiya — sirf is run ke liye.



### 2. RUN LEVEL
```bash
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

gemini_api_key = ""

#Reference: https://ai.google.dev/gemini-api/docs/openai
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

agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Hello, how are you.", run_config=config)

print(result.final_output)
```

### GLOBAL
```bash
from agents import Agent, Runner, AsyncOpenAI, set_default_openai_client, set_tracing_disabled, set_default_openai_api

gemini_api_key = ""
set_tracing_disabled(True)
set_default_openai_api("chat_completions")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_default_openai_client(external_client)

agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model="gemini-2.0-flash")

result = Runner.run_sync(agent, "Hello")

print(result.final_output)
```