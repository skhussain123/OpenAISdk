
#### Tools type
custom function likhy or uska schemea likhty hain. kisi bhi function me @decorator laga kr tool me convert krle..
hosted tool jo pechy le bany howy ho, ---> third party hosted tool
file search tool alternative(custom rag system)
computer operator preview model alternative(Browser use)
open


#### Agent 4 cheezy leta haer
* system promt
* user prompt
* tool schema
* final tool ka answer ho wapis agent ke pass jata hain

## Context management

Agents SDK me context aik central system hota hai jo agents ke darmiyan data share karne, tools use karne aur memory maintain karne ke liye use hota hai.

Context wo additional maloomat hoti hai jo hum apne LLM ya agent ko dete hain — taake wo apna kaam zyada samajhdari se kar sake. Ye information LLM ke paas naturally nahi hoti, is liye humein manually deni padti hai. Jaise agar user ka naam, unki preferences, unka pehla message, koi external tool se aayi information (jaise weather data, database records, ya health status) — in sab ko hum agent ko context ke taur par dete hain. Jab agent loop chalta hai aur beech mein tools call hotay hain, ya external sources se data fetch hota hai, aur wo data agent ko diya jata hai taake agla decision usi base par ho — to ye poora process context sharing kehlata hai. Is context ke zariye agent ko “yaad” rahta hai ke pehle kya ho chuka hai, user ka maksad kya hai, aur kaun se tools ya steps involve ho chuke hain. Yani context basically agent ka working memory hoti hai jo har interaction ko meaningful banati hai.

### Context Dene ke 3 Tareeqay (OpenAI Agents SDK / LLMs)

Context, jo ke AI agent ko samajhne aur intelligent response dene mein madad karta hai, hum teen mukhtalif tareeqon se provide kar sakte hain:

1. System Prompt: Ye ek initial instruction hota hai jo agent ko batata hai ke uska role kya hai, tone kaisi honi chahiye, aur kis tarah ka behavior expect kiya ja raha hai. Jaise: "You are a helpful legal assistant." — ye prompt agent ke reasoning ka base tay karta hai.

2. User Input Prompt: Jab user koi query bhejta hai, wo bhi context ka ek hissa hota hai. Ye prompt dynamic hota hai, har interaction ke saath change hota hai, aur agent ko batata hai ke abhi kya karna hai. Jaise: "Mujhe Lahore ka weather batao."

3. External Functions / Tools / APIs: Jab agent kisi external source se data fetch karta hai — jaise web search, database query, ya kisi tool ka result — to wo information bhi agent ke liye context ban jati hai. Ye context agent loop mein automatically add hoti hai taake aane wale response usi ke base par ho. Example: web search result: "Lahore weather is 34°C and sunny."


#### User Profile Management Third Party Tool
https://mem0.ai/


Context is an overloaded term. There are two main classes of context you might care about:

Context available locally to your code: this is data and dependencies you might need when tool functions run, during callbacks like on_handoff, in lifecycle hooks, etc.
Context available to LLMs: this is data the LLM sees when generating a response.

### 1. Local context
Ye wo context hota hai jo sirf aapke Python code ke liye hota hai, LLM isay nahi dekhta. Ye context aap use karte ho:

* Jab koi tool function chal raha hota hai
* Jab on_handoff(), on_step_start(), on_step_end() jaise callback hooks chalte hain
* Jab aapko user ID, token, ya environment variable zarurat ho tool ke andar
* API key, config, ya backend ka internal data
* Ye context sirf code ke liye hota hai, model ke liye nahi.


This is represented via the RunContextWrapper class and the context property within it. The way this works is:

1. You create any Python object you want. A common pattern is to use a dataclass or a Pydantic object.
2. You pass that object to the various run methods (e.g. Runner.run(..., **context=whatever**)).
3. All your tool calls, lifecycle hooks etc will be passed a wrapper object, RunContextWrapper[T], where T represents your context object type which you can access via wrapper.context.

The most important thing to be aware of: every agent, tool function, lifecycle etc for a given agent run must use the same type of context.

* Contextual data for your run (e.g. things like a username/uid or other information about the user)
* Dependencies (e.g. logger objects, data fetchers, etc)
* Helper functions


```bash
import asyncio
from dataclasses import dataclass

from agents import Agent, RunContextWrapper, Runner, function_tool

@dataclass
class UserInfo:  
    name: str
    uid: int

@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:  
    """Fetch the age of the user. Call this function to get user's age information."""
    return f"The user {wrapper.context.name} is 47 years old"

async def main():
    user_info = UserInfo(name="John", uid=123)

    agent = Agent[UserInfo](  
        name="Assistant",
        tools=[fetch_user_age],
    )

    result = await Runner.run(  
        starting_agent=agent,
        input="What is the age of the user?",
        context=user_info,
    )

    print(result.final_output)  
    # The user John is 47 years old.

if __name__ == "__main__":
    asyncio.run(main())

```

#### Second Example 
```bash
import asyncio
from dataclasses import dataclass

from agents import Agent, RunContextWrapper, Runner, function_tool

@dataclass
class UserInfo1:
    name: str
    uid: int
    location: str = "Pakistan"

@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo1]) -> str:
    '''Returns the age of the user.'''
    return f"User {wrapper.context.name} is 30 years old"

@function_tool
async def fetch_user_location(wrapper: RunContextWrapper[UserInfo1]) -> str:
    '''Returns the location of the user.'''
    return f"User {wrapper.context.name} is from {wrapper.context.location}"

async def main():
    user_info = UserInfo1(name="Muhammad Qasim", uid=123)

    agent = Agent[UserInfo1](
        name="Assistant",
        tools=[fetch_user_age,fetch_user_location],
        model=model
    )

    result = await Runner.run(
        starting_agent=agent,
        input="What is the age of the user? current location of his/her?",
        context=user_info,
    )

    print(result.final_output)
    # The user John is 47 years old.

if __name__ == "__main__":
    asyncio.run(main())
```   
##### Output
The user is 30 years old and is from Pakistan. 

#### Dynamic Instructions with context
```bash
import asyncio
import random
from typing import Literal

from agents import Agent, RunContextWrapper, Runner

class CustomContext:
    def __init__(self, style: Literal["haiku", "pirate", "robot"]):
        self.style = style


def custom_instructions(
    run_context: RunContextWrapper[CustomContext], agent: Agent[CustomContext]
) -> str:
    context = run_context.context
    if context.style == "haiku":
        return "Only respond in haikus."
    elif context.style == "pirate":
        return "Respond as a pirate."
    else:
        return "Respond as a robot and say 'beep boop' a lot."


agent = Agent(
    name="Chat agent",
    instructions=custom_instructions,
    model=model
)


async def main():
    choice: Literal["haiku", "pirate", "robot"] = random.choice(["haiku", "pirate", "robot"])
    context = CustomContext(style=choice)
    print(f"Using style: {choice}\n")

    user_message = "Tell me a joke."
    print(f"User: {user_message}")
    result = await Runner.run(agent, user_message, context=context)

    print(f"Assistant: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
```
##### Output
Using style: haiku

User: Tell me a joke.
Assistant: Why did the scarecrow
Win an award? Because he was
Outstanding in his field.

### Usingpydantic 
```bash
import asyncio
from pydantic import BaseModel

from agents import Agent, RunContextWrapper, Runner, function_tool

# ✅ Pydantic BaseModel use kiya gaya hai
class UserInfo(BaseModel):  
    name: str
    uid: int

@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:  
    """Fetch the age of the user. Call this function to get user's age information."""
    return f"The user {wrapper.context.name} is 47 years old"

async def main():
    user_info = UserInfo(name="John", uid=123)

    agent = Agent[UserInfo](  
        name="Assistant",
        tools=[fetch_user_age],
    )

    result = await Runner.run(  
        starting_agent=agent,
        input="What is the age of the user?",
        context=user_info,
    )

    print(result.final_output)  
    # Output: The user John is 47 years old.

if __name__ == "__main__":
    asyncio.run(main())

```

### 2. Agent/LLM context

Ye wo context hota hai jo directly LLM ko diya jata hai — aur ye uske jawab banane mein help karta hai. Ismein shamil hota hai:
* System Prompt: LLM ko role ya instruction batana
* User Input Prompt: Jo user ne kaha
* Tool ka Output: Agar kisi tool ne response diya, to wo bhi context ban jata hai
* Memory ya Conversation History: Pehle kya baat hui, wo bhi context hai
*  LLM is context ko directly dekhta hai aur usi base par jawab deta hai.

| Type          | Kis ke liye hai?    | LLM ko visible? | Use Kahan Hota Hai?                         |
| ------------- | ------------------- | --------------- | ------------------------------------------- |
| Local Context | Python code ke liye | ❌ Nahin         | Tools, callbacks, config, internal logic    |
| LLM Context   | LLM ke liye         | ✅ Haan          | Prompt, memory, tool output, agent messages |


### Data LLM ko dene ke 4 tareeqe:

* Isay "developer message" ya "system prompt" bhi kehte hain.
* Yeh static string ya dynamic function ho sakta hai.
* Har baar agent run hota hai, yeh message LLM ko diya jata hai.
* Example: User ka naam, current date, ya instructions jese:
“User ka naam Ali hai. Use short aur polite answers do.”


###  Input ke zariye (Runner.run ke input me)

* Jab Runner.run() call karte ho, to input me data send kar sakte ho.
* Yeh system prompt se neeche level ka message hota hai.
* Zyada customized ya temporary data bhejne ke liye use hota hai.


### Function Tools ke zariye (on-demand data)
* LLM ko agar koi info chahiye, to wo function tool ko call karke data le sakta hai.
* Example: get_user_profile() tool call karke user info fetch kar lena.
* Yeh tab kaam aata hai jab data real-time ya dynamic ho.

### Retrieval ya Web Search Tools

* Retrieval: Files, databases ya documents se relevant data fetch karta hai.
* Web Search: Internet se live data laata hai.
* Yeh grounding ke liye use hota hai – yani jawab accurate aur real data par based ho.


### Summary
LLM sirf wahi data dekh sakta hai jo uske conversation history me ho — is liye agar aap extra info dena chahte ho, to usay prompt, input, tool, ya retrieval ke zariye model ke saamne lana hota hai.


### Agent/LLM context
```bash
import asyncio
from dataclasses import dataclass
from agents import enable_verbose_stdout_logging

from agents import Agent, RunContextWrapper, Runner, function_tool

enable_verbose_stdout_logging()

@dataclass
class UserInfo:
    name: str
    uid: int

@function_tool
async def greet_user(context: RunContextWrapper[UserInfo], greeting: str) -> str:
  """Greets the User with their name.
  Args:
    greeting: A specialed greeting message for user
  """
  name = context.context.name
  return f"Hello {name}, {greeting}"

async def main():
    user_info = UserInfo(name="Muhammad Qasim", uid=123)

    agent = Agent[UserInfo](
        name="Assistant",
        tools=[greet_user],
        model=model,
        # Dynamic function context pass in instructions/system prompmt/developer prompt
        instructions="Always greet the user using <function_call>greet_user</function_call> and welcome them to Panaversity"
    )

    result = await Runner.run(
        starting_agent=agent,
        input="Hello",
        context=user_info,
    )

    print(result.final_output)

asyncio.run(main())
```

##### Output:
```bash
Tracing is disabled. Not creating trace Agent workflow
DEBUG:openai.agents:Tracing is disabled. Not creating trace Agent workflow
Setting current trace: no-op
DEBUG:openai.agents:Setting current trace: no-op
Tracing is disabled. Not creating span <agents.tracing.span_data.AgentSpanData object at 0x7a07754cc5f0>
DEBUG:openai.agents:Tracing is disabled. Not creating span <agents.tracing.span_data.AgentSpanData object at 0x7a07754cc5f0>
Running agent Assistant (turn 1)
DEBUG:openai.agents:Running agent Assistant (turn 1)
Tracing is disabled. Not creating span <agents.tracing.span_data.GenerationSpanData object at 0x7a07754cc890>
DEBUG:openai.agents:Tracing is disabled. Not creating span <agents.tracing.span_data.GenerationSpanData object at 0x7a07754cc890>
[
  {
    "content": "Always greet the user using <function_call>greet_user</function_call> and welcome them to Panaversity",
    "role": "system"
  },
  {
    "role": "user",
    "content": "Hello"
  }
]
Tools:
[
  {
    "type": "function",
    "function": {
      "name": "greet_user",
      "description": "Greets the User with their name.\nArgs:\n  greeting: A specialed greeting message for user",
      "parameters": {
        "properties": {
          "greeting": {
            "title": "Greeting",
            "type": "string"
          }
        },
        "required": [
          "greeting"
        ],
        "title": "greet_user_args",
        "type": "object",
        "additionalProperties": false
      }
    }
  }
]
Stream: False
Tool choice: NOT_GIVEN
Response format: NOT_GIVEN

DEBUG:openai.agents:[
  {
    "content": "Always greet the user using <function_call>greet_user</function_call> and welcome them to Panaversity",
    "role": "system"
  },
  {
    "role": "user",
    "content": "Hello"
  }
]
Tools:
[
  {
    "type": "function",
    "function": {
      "name": "greet_user",
      "description": "Greets the User with their name.\nArgs:\n  greeting: A specialed greeting message for user",
      "parameters": {
        "properties": {
          "greeting": {
            "title": "Greeting",
            "type": "string"
          }
        },
        "required": [
          "greeting"
        ],
        "title": "greet_user_args",
        "type": "object",
        "additionalProperties": false
      }
    }
  }
]
Stream: False
Tool choice: NOT_GIVEN
Response format: NOT_GIVEN

LLM resp:
{
  "content": null,
  "refusal": null,
  "role": "assistant",
  "annotations": null,
  "audio": null,
  "function_call": null,
  "tool_calls": [
    {
      "id": "",
      "function": {
        "arguments": "{\"greeting\":\"Welcome to Panaversity!\"}",
        "name": "greet_user"
      },
      "type": "function"
    }
  ]
}

DEBUG:openai.agents:LLM resp:
{
  "content": null,
  "refusal": null,
  "role": "assistant",
  "annotations": null,
  "audio": null,
  "function_call": null,
  "tool_calls": [
    {
      "id": "",
      "function": {
        "arguments": "{\"greeting\":\"Welcome to Panaversity!\"}",
        "name": "greet_user"
      },
      "type": "function"
    }
  ]
}

Tracing is disabled. Not creating span <agents.tracing.span_data.FunctionSpanData object at 0x7a07754ccb90>
DEBUG:openai.agents:Tracing is disabled. Not creating span <agents.tracing.span_data.FunctionSpanData object at 0x7a07754ccb90>
Invoking tool greet_user with input {"greeting":"Welcome to Panaversity!"}
DEBUG:openai.agents:Invoking tool greet_user with input {"greeting":"Welcome to Panaversity!"}
Tool call args: ['Welcome to Panaversity!'], kwargs: {}
DEBUG:openai.agents:Tool call args: ['Welcome to Panaversity!'], kwargs: {}
Tool greet_user returned Hello Muhammad Qasim, Welcome to Panaversity!
DEBUG:openai.agents:Tool greet_user returned Hello Muhammad Qasim, Welcome to Panaversity!
Running agent Assistant (turn 2)
DEBUG:openai.agents:Running agent Assistant (turn 2)
Tracing is disabled. Not creating span <agents.tracing.span_data.GenerationSpanData object at 0x7a07754ccbf0>
DEBUG:openai.agents:Tracing is disabled. Not creating span <agents.tracing.span_data.GenerationSpanData object at 0x7a07754ccbf0>
[
  {
    "content": "Always greet the user using <function_call>greet_user</function_call> and welcome them to Panaversity",
    "role": "system"
  },
  {
    "role": "user",
    "content": "Hello"
  },
  {
    "role": "assistant",
    "tool_calls": [
      {
        "id": "",
        "type": "function",
        "function": {
          "name": "greet_user",
          "arguments": "{\"greeting\":\"Welcome to Panaversity!\"}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "tool_call_id": "",
    "content": "Hello Muhammad Qasim, Welcome to Panaversity!"
  }
]
Tools:
[
  {
    "type": "function",
    "function": {
      "name": "greet_user",
      "description": "Greets the User with their name.\nArgs:\n  greeting: A specialed greeting message for user",
      "parameters": {
        "properties": {
          "greeting": {
            "title": "Greeting",
            "type": "string"
          }
        },
        "required": [
          "greeting"
        ],
        "title": "greet_user_args",
        "type": "object",
        "additionalProperties": false
      }
    }
  }
]
Stream: False
Tool choice: NOT_GIVEN
Response format: NOT_GIVEN

DEBUG:openai.agents:[
  {
    "content": "Always greet the user using <function_call>greet_user</function_call> and welcome them to Panaversity",
    "role": "system"
  },
  {
    "role": "user",
    "content": "Hello"
  },
  {
    "role": "assistant",
    "tool_calls": [
      {
        "id": "",
        "type": "function",
        "function": {
          "name": "greet_user",
          "arguments": "{\"greeting\":\"Welcome to Panaversity!\"}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "tool_call_id": "",
    "content": "Hello Muhammad Qasim, Welcome to Panaversity!"
  }
]
Tools:
[
  {
    "type": "function",
    "function": {
      "name": "greet_user",
      "description": "Greets the User with their name.\nArgs:\n  greeting: A specialed greeting message for user",
      "parameters": {
        "properties": {
          "greeting": {
            "title": "Greeting",
            "type": "string"
          }
        },
        "required": [
          "greeting"
        ],
        "title": "greet_user_args",
        "type": "object",
        "additionalProperties": false
      }
    }
  }
]
Stream: False
Tool choice: NOT_GIVEN
Response format: NOT_GIVEN

LLM resp:
{
  "content": "Hello Muhammad Qasim, Welcome to Panaversity!\n",
  "refusal": null,
  "role": "assistant",
  "annotations": null,
  "audio": null,
  "function_call": null,
  "tool_calls": null
}

DEBUG:openai.agents:LLM resp:
{
  "content": "Hello Muhammad Qasim, Welcome to Panaversity!\n",
  "refusal": null,
  "role": "assistant",
  "annotations": null,
  "audio": null,
  "function_call": null,
  "tool_calls": null
}

Resetting current trace
DEBUG:openai.agents:Resetting current trace
Hello Muhammad Qasim, Welcome to Panaversity!

```

```bash
import asyncio
from dataclasses import dataclass

from agents import Agent, RunContextWrapper, Runner, function_tool

@dataclass
class UserInfo:
    name: str
    uid: int

@function_tool
async def greet_user(context: RunContextWrapper[UserInfo], greeting: str) -> str:
  """Greets the User with their name.
  Args:
    greeting: A specialed greeting message for user
  """
  name = context.context.name
  return f"Hello {name}, {greeting}"

async def main():
    user_info = UserInfo(name="Junaid", uid=123)

    agent = Agent[UserInfo](
        name="Assistant",
        tools=[greet_user],
        model=model,
        instructions="Always greet the user using <function_call>greet_user</function_call> and welcome them to Panaversity"
    )

    result = await Runner.run(
        starting_agent=agent,
        input="Hello",
        context=user_info,
    )

    print(result.final_output)

asyncio.run(main())
```
