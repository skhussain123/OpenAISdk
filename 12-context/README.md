

## Context management

Agents SDK me context aik central system hota hai jo agents ke darmiyan data share karne, tools use karne aur memory maintain karne ke liye use hota hai.


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