

### What is Context 
Context ka matlab hai. Agent ke paas kya maaloomat hai jo uske faislay lene mein madad karti hai.

#### Jese
* User ne pehle kya bola tha
* System instructions kya hain
* Agent ke paas konsi tools hain
* Memory ya kisi file se mila huwa data

Ye sab milke agent ka dimaag banate hain.

### Context Ki Importance Kya Hai

* Samajh sakta hai ke user kya chah raha hai.
* Sahi tool choose karta hai (jaise weather check karna ho to weather_tool).
* Pichlay baat ya queries ko yaad rakhta hai.
* Multi-step kaam (pehle summarize, phir email) perform kar sakta hai.

##### Agar context na ho:
Agent hamesha confused hoga, ghalat tools use karega, aur jawab random lagega.


### Context Kis Tarah Use Hota Hai (Code Ke Andar)

1. System instructions — Agent ka role set hota hai ("Tum ek essay writer ho").
2. User ka message — Har naya input context ka hissa banta hai.
3. Tool ka meta data — Jaise tool ka naam, description, aur kaam kya hai.
4. Memory / History — Agar enable ho, to agent ko yaad rehta hai ke user ne pehle kya bola.

* Yeh sab combine ho kar agent ko guide karta hai ke ab kya karna hai.


### Multi-Agent Me Context Ka Role
Jab kai agents kaam kar rahe hote hain:

* Har agent apna context share karta hai (Model Context Protocol - MCP).
* Ye ensure karta hai ke agents ek dusray ko samajh saken.


### Summary 

* Context = Agent ka dimaag + yaad-dasht
* Ye decide karta hai:
  * Konsa tool use hoga
  * Konsi language me jawab dena hai
  * Pichli baat yaad hai ya nahi

* Agar context sahi set ho to agent kaam smart tareeqay se karta hai


Context management in the OpenAI Agents SDK refers to handling additional data that your code can use during an agent’s execution. This “context” comes in two main forms:

### 1. Local Context
Woh maloomat (instructions, tools, ya variables) jo sirf ek agent ya ek function ke andar hoti hain – aur baahar ke agents ya tools usay directly access nahi kar saktay.

#### How It Works:
#####  Creating Context:
You create a Python object—often using a dataclass or a Pydantic model—to encapsulate data like a username, user ID, logger, or helper functions.

##### Passing Context:
You pass this object to the run method (e.g., Runner.run(..., context=your_context)). The SDK wraps your object in a RunContextWrapper, making it available to every tool function, lifecycle hook, or callback during that run via wrapper.context.

##### Key Point:
All parts of a single agent run must share the same type of context, ensuring consistency.


#### Example Use Cases
* Storing user details (e.g., a username or ID) that your tools might need.
* Injecting dependencies such as loggers or data fetchers.
* Providing helper functions accessible throughout the run.

Note: This local context is not exposed to the LLM. It’s solely for your backend logic and operations.

### 2. Agent/LLM Context
Ye wo data ya maloomat hoti hai jo AI model (LLM) ko direct dikhayi jati hai — jise dekh kar wo response banata hai.

Isme yeh cheezein shamil hoti hain:
* System instructions (e.g., “tum ek English teacher ho”)
* User ka input (e.g., “Mujhe essay likh ke do”)
* Conversation history (pichlay sawal/jawabat)

#### How to Use It:
##### Embedding in Instructions:
Include important context (like the user’s name, current date, or specific guidelines) directly in the agent’s instructions or system prompts.

##### Passing in Inputs:
You can also add context to the input message when calling Runner.run(), ensuring that this data is part of the conversation that the LLM processes.

##### Function Tools:
The LLM may also invoke function tools to fetch on-demand data that wasn’t initially part of its conversation history.

##### Retrieval/Web Search:
Use specialized tools to pull in relevant external data, thereby grounding the LLM’s responses in up-to-date or detailed information.

##### Key Difference:
While the local context is internal and never sent to the LLM, the agent/LLM context is deliberately exposed as part of the conversation to influence and guide the LLM’s response generation.

### Code Example Breakdown
Consider the following simplified example that demonstrates local context management:
```bash
import asyncio
from dataclasses import dataclass

from agents import Agent, RunContextWrapper, Runner, function_tool

# Define a simple context using a dataclass
@dataclass
class UserInfo:  
    name: str
    uid: int

# A tool function that accesses local context via the wrapper
@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:  
    return f"User {wrapper.context.name} is 47 years old"

async def main():
    # Create your context object
    user_info = UserInfo(name="John", uid=123)  

    # Define an agent that will use the tool above
    agent = Agent[UserInfo](  
        name="Assistant",
        tools=[fetch_user_age],
    )

    # Run the agent, passing in the local context
    result = await Runner.run(
        starting_agent=agent,
        input="What is the age of the user?",
        context=user_info,
    )

    print(result.final_output)  # Expected output: The user John is 47 years old.

if __name__ == "__main__":
    asyncio.run(main())

```


Yeh code tumhare backend ke liye local context use karta hai (jaise user ka naam aur ID), jisko LLM ko nahi dikhaya jata, lekin tools use kar sakte hain.

### Step-by-Step

#### Step 1: Import aur Dataclass Setup
```bash
from dataclasses import dataclass
```
* Hum UserInfo naam ka ek custom Python object (dataclass) bana rahe hain — jisme hum user ki info store karenge (naam aur UID).
```bash
@dataclass
class UserInfo:  
    name: str
    uid: int
```
* Matlab: Yeh structure tumhare backend tools ko batayega ke user ka naam aur ID kya hai.

#### Step 2: Tool Function Banana
```bash
@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:  
    return f"User {wrapper.context.name} is 47 years old"
```
* @function_tool: Is function ko tool bana diya gaya hai jo AI agent call karega.
* wrapper.context.name: Yeh wahi context hai jo tum backend se pass karte ho. Yahaan se user ka naam mil raha hai.

LLM ko ye context nahi dikh raha, sirf tool isay internally use kar raha hai.

#### Step 3: Agent Define Karna
```bash
agent = Agent[UserInfo](
    name="Assistant",
    tools=[fetch_user_age],
)
```
* Yeh agent banaya gaya hai jo fetch_user_age tool use karega.
* Agent[UserInfo] ka matlab: ye agent UserInfo type context expect karta hai.

#### Step 4: Runner Se Execute Karna
```bash
user_info = UserInfo(name="John", uid=123)
```
* Yeh tumhara local context object hai — jise tum run ke waqt pass karoge.

```bash
result = await Runner.run(
    starting_agent=agent,
    input="What is the age of the user?",
    context=user_info,
)
```
* Yahan tum Runner.run() se agent chala rahe ho, aur usko user ka data bhi de rahe ho.

#### Final Output:
```bash
print(result.final_output)
```

Tumne ek UserInfo context banaya, tool ke zariye uska naam use karke response diya, bina LLM ko wo context directly diye.

