
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
* final tool ka answer dety ha llm ko



## Context management

Agents SDK me context aik central system hota hai jo agents ke darmiyan data share karne, tools use karne aur memory maintain karne ke liye use hota hai.

Context wo additional maloomat hoti hai jo hum apne LLM ya agent ko dete hain — taake wo apna kaam zyada samajhdari se kar sake. Ye information LLM ke paas naturally nahi hoti, is liye humein manually deni padti hai. Jaise agar user ka naam, unki preferences, unka pehla message, koi external tool se aayi information (jaise weather data, database records, ya health status) — in sab ko hum agent ko context ke taur par dete hain. Jab agent loop chalta hai aur beech mein tools call hotay hain, ya external sources se data fetch hota hai, aur wo data agent ko diya jata hai taake agla decision usi base par ho — to ye poora process context sharing kehlata hai. Is context ke zariye agent ko “yaad” rahta hai ke pehle kya ho chuka hai, user ka maksad kya hai, aur kaun se tools ya steps involve ho chuke hain. Yani context basically agent ka working memory hoti hai jo har interaction ko meaningful banati hai.

### Context Dene ke 3 Tareeqay (OpenAI Agents SDK / LLMs)

Context, jo ke AI agent ko samajhne aur intelligent response dene mein madad karta hai, hum teen mukhtalif tareeqon se provide kar sakte hain:

1. System Prompt: Ye ek initial instruction hota hai jo agent ko batata hai ke uska role kya hai, tone kaisi honi chahiye, aur kis tarah ka behavior expect kiya ja raha hai. Jaise: "You are a helpful legal assistant." — ye prompt agent ke reasoning ka base tay karta hai.

2. User Input Prompt: Jab user koi query bhejta hai, wo bhi context ka ek hissa hota hai. Ye prompt dynamic hota hai, har interaction ke saath change hota hai, aur agent ko batata hai ke abhi kya karna hai. Jaise: "Mujhe Lahore ka weather batao."

3. External Functions / Tools / APIs: Jab agent kisi external source se data fetch karta hai — jaise web search, database query, ya kisi tool ka result — to wo information bhi agent ke liye context ban jati hai. Ye context agent loop mein automatically add hoti hai taake aane wale response usi ke base par ho. Example: web search result: "Lahore weather is 34°C and sunny."
























### 1. Context kya hota hai?
Jab aik agent run hota hai, to context automatically create ho jata hai.

* user_id: Wo user jo agent se baat kar raha hai
* session_id: Har session ya conversation ka unique ID
* memory: Temporary data store karne ke liye (key-value jese dictionary)
* tools: Available tools (handoff tools bhi isme hotay hain)
* agent_name: Abhi kaunsa agent run ho raha hai


### 2. Context ka istemal kahan hota hai

| Istemaal                               | Faida                                                       |
| -------------------------------------- | ----------------------------------------------------------- |
| Agents ke darmiyan info share karna    | `context.memory["key"] = value` use karo                    |
| Dusre agent ke tools use karna         | `context.tools["tool_name"]` se tool ko access karo         |
| Data ya logic dynamically change karna | `memory` me value daal ke agent ka behaviour badal sakte ho |
| User ya session info track karna       | `context.user_id` aur `session_id` se                       |


### 3. Memory kya hoti hai
* Memory bilkul dictionary jesi hoti hai: context.memory["x"] = y
* Yeh saari run ke dauraan active rehti hai
* Multiple agents ke beech yeh data share karta hai


### Summary

* Context aik shared memory aur tool box hota hai agent ke liye
* Data store karna, tools access karna aur info pass karna iske zariye hota hai
* Iska istemal agents ke darmiyan coordination aur data flow ke liye hota hai
* Use: context.memory["key"] = value, context.tools["tool"], context.user_id


## Agent / LLM Context
Jab aik LLM (Language Model) ko call kiya jata hai, to wo sirf wahi data dekh sakta hai jo conversation history me hota hai. Agar aap chahte ho ke koi naya data model ko dikhai de, to usay history ka part banana zaroori hai.

### Data LLM ko dene ke 4 tareeqe:

* Isay "developer message" ya "system prompt" bhi kehte hain.
* Yeh static string ya dynamic function ho sakta hai.
8 Har baar agent run hota hai, yeh message LLM ko diya jata hai.
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


## RunContext

```bash

# Define your custom context
@dataclass
class UserInfo:
    name: str
    uid: int

# Tool that uses local context
@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:
    return f"User {wrapper.context.name} is 47 years old."

# Agent that uses the context-aware tool
agent = Agent[UserInfo](
    name="Assistant",
    tools=[fetch_user_age],
    model=model
)

# Main runner
async def main():
    # Create your context
    user_info = UserInfo(name="Ali", uid=101)

    # Run the agent
    result = await Runner.run(
        starting_agent=agent,
        input="What is the age of the user?",
        context=user_info,
        run_config=config
    )

    print("\n Final Output:\n", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

```

