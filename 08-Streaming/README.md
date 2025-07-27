
### what is streaming in openai sdk
In the OpenAI SDK, streaming refers to the ability to receive the response from the model token-by-token (or chunk-by-chunk) as it's generated, instead of waiting for the entire response to complete before you get any output.


### Why Use Streaming?

* Faster feedback: You see results instantly as they are generated.
* Better user experience: Useful in chat apps, terminals, or any interactive UI.
* Ideal for long responses: Reduces perceived latency for long outputs.

### Synchronous
Synchronous mode mein jab user koi query karta hai, to poori request server tak bheji jati hai aur server usay process karta hai. Lekin jab tak poora jawab tayar nahi ho jata, tab tak user ko kuch bhi response nahi milta. Server jab apna kaam mukammal kar leta hai, tabhi ek baar mein poora output wapas bhejta hai. Is tarah ka system tab theek hota hai jab response chhota ho ya real-time feedback ki zarurat na ho.

Iske muqable mein asynchronous ya streaming mode mein data tukdon (chunks) mein wapas aata hai. Jaise hi server kuch output generate karta hai, wo foran user ko bhejna shuru kar deta hai. Poore response ka intezar nahi hota. Yeh approach un situations mein bohot faida mand hoti hai jahan response lamba ho ya user ko turant feedback dikhana ho – jaise AI chat apps ya terminal-based tools mein. Streaming se user ko lagta hai ke system fast aur responsive hai, kyunke output foran dikhna shuru ho jata hai.

### Asynchronous
Asynchronous (ya async) mode mein jab user koi query bhejta hai, to server usay process karna start karta hai lekin poore response ka intezar nahi karta. Jaise hi model kuch output generate karta hai, wo usay chunks (tukdon) mein turant wapas bhejna shuru kar deta hai. Iska matlab hai ke user ko pehla hissa foran mil jata hai, phir agla, phir uske baad wala — jab tak poora jawab complete nahi ho jata. Is process ko streaming kehte hain. Async mode ka faida ye hai ke user ko real-time feedback milta hai, aur response jaldi aur smooth lagta hai. Ye approach un apps ke liye ideal hoti hai jahan AI se lambi conversation hoti hai, jaise chatbots, assistants, ya terminal tools, jahan har second kaafi important hota hai.


Jab humara agent loop mein continuously tool calls ya LLM calls kar raha hota hai, to wo asynchronous tareeqay se kaam karta hai — khas kar jab hum streaming ka use karte hain.

###  Kaise hota hai async behavior agent loop mein?

1. Agent runner ya loop continuously input le raha hota hai aur usko process karne ke liye LLM ya tools ko forward kar raha hota hai.
2. Jab agent ko koi tool call karni hoti hai (e.g. weather tool, calculator, DB lookup), wo non-blocking tareeqay se async call karta hai.
3. Isi tarah, jab LLM (OpenAI ya koi aur) ko call karta hai with streaming, to response chunks mein wapas aata hai, real-time mein.


###  1. runner.run(prompt)
🔹 Purpose: Query bhejna aur complete response aik baar mein lena.
🔹 Nature: Asynchronous (await karna parta hai).
🔹 Use-case: Jab aapko full result aik hi baar mein chahiye ho.

### 2. runner.run_sync(prompt)
🔹 Purpose: Same as run(), but sync code ke liye.
🔹 Nature: Synchronous (without async/await).
🔹 Use-case: Jab aap ka code async nahi hai (like simple scripts or CLI).


### 3. runner.stream(prompt)
🔹 Purpose: Prompt bhejna aur real-time streaming mein response lena.
🔹 Nature: Asynchronous stream (token/token ya chunk/chunk mein response aata hai).
🔹 Use-case: Chat apps, terminals, jahan user ko live output chahiye hota hai.


| Method              | Async / Sync | Streaming | Output Type     | Use When                             |
| ------------------- | ------------ | --------- | --------------- | ------------------------------------ |
| `runner.run()`      | Async        | ❌         | Full message    | Full output after processing         |
| `runner.stream()`   | Async        | ✅         | Streamed chunks | Real-time / token-by-token output    |
| `runner.run_sync()` | Sync         | ❌         | Full message    | When not using async (basic scripts) |


#### runner.run_sync vs runner.run
1. runner.run() ek asynchronous function ko run karta hai runner ke context ke andar.
Isse await ke saath call kiya jata hai, aur yeh async code ke liye hota hai.
2. Same as run(), but sync code ke liye. Nature: Synchronous (without async/await).

#### Key Points
* await ko humesha async funciton ke under use kia jata hain
* async function ko call krwany ke liye await lagana pharta hain.
* async.io ki library async function ko run krny ke liye use hoti hain.

### run_streamed
run_streamed() is a higher-level helper in the OpenAI Agents SDK that gives you real-time streaming (like stream()), but with the final assembled response object at the end.


```bash
import asyncio

from openai.types.responses import ResponseTextDeltaEvent

from agents import Agent, Runner


async def main():
    agent = Agent(
        name="Joker",
        instructions="You are a helpful assistant.",
        model=model
    )

    result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)



asyncio.run(main())
```

### stream_events()
stream_events() is a low-level method in the OpenAI Agents SDK that streams internal agent events, not just plain message content.

```bash
import asyncio
import random

from agents import Agent, ItemHelpers, Runner, function_tool


@function_tool
def how_many_jokes() -> int:
    return random.randint(1, 10)


async def main():
    agent = Agent(
        name="Joker",
        instructions="First call the `how_many_jokes` tool, then tell that many jokes.",
        tools=[how_many_jokes],
        model=model
    )

    result = Runner.run_streamed(
        agent,
        input="Hello",

    )
    print("=== Run starting ===")
    async for event in result.stream_events():
        # We'll ignore the raw responses event deltas
        if event.type == "raw_response_event":
            continue
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass  # Ignore other event types

asyncio.run(main())

print("=== Run complete ===")
```

#### Type of Event
* agent_updated_stream_event
* raw_response_event
* run_item_stream_event



### 1. Raw response events
RawResponsesStreamEvent are raw events passed directly from the LLM. They are in OpenAI Responses API format, which means each event has a type (like response.created, response.output_text.delta, etc) and data. These events are useful if you want to stream response messages to the user as soon as they are generated.

```bash
result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
```            


### 2. Run item events 
```bash
 elif event.type == "run_item_stream_event":   
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
                continue
            elif event.item.type == "tool_call_output_item":
                # print(f"-- Tool output: {event.item.output}")
                continue
            elif event.item.type == "message_output_item":
                # print(event.item.raw_item.content[0].text)
                # print(ItemHelpers.text_message_output(event.item))
                continue
```                

### 3. agent events
```bash
 elif event.type == "agent_updated_stream_event":
        #    print(event)
           continue
```

### Other Code Example 
```bash
import os
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import (
    Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,
    RunConfig,ItemHelpers, function_tool
)
import requests

from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()


gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")


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
    model_provider=external_client
)


@function_tool
def get_weather(city:str)->str:
    """
    Get the current weather for a given city.
    """
    result=requests.get(f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}")
    data=result.json()
    return f"The current weather in {city} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."


async def main():
    
    agent = Agent(
    name="Weather Agent",
    instructions="You are a weather agent. You can provide weather information and forecasts.",
    model=model,
    tools=[get_weather]
    )

    result = Runner.run_streamed(agent, input="what is weather in karachi.")
    async for event in result.stream_events():
       if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            # print(event.data.delta, end="", flush=True)
            continue
       elif event.type == "agent_updated_stream_event":
        #    print(event)
           continue
       
       elif event.type == "run_item_stream_event":   
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
                continue
            elif event.item.type == "tool_call_output_item":
                # print(f"-- Tool output: {event.item.output}")
                continue
            elif event.item.type == "message_output_item":
                # print(event.item.raw_item.content[0].text)
                # print(ItemHelpers.text_message_output(event.item))
                continue


asyncio.run(main())
```