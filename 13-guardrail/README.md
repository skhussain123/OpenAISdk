

### Guardrails
Guardrails run in parallel to your agents, enabling you to do checks and validations of user input. For example, imagine you have an agent that uses a very smart (and hence slow/expensive) model to help with customer requests. You wouldn't want malicious users to ask the model to help them with their math homework. So, you can run a guardrail with a fast/cheap model. If the guardrail detects malicious usage, it can immediately raise an error, which stops the expensive model from running and saves you time/money.

#### There are two kinds of guardrails:
1. Input guardrails run on the initial user input
2. Output guardrails run on the final agent output


```bash
uv add pydantic
```

#### agr ap chahty ha apka agent structure output de. to pydantic structure output deny ke help krygi
```bash
import asyncio
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import (
    Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, set_tracing_disabled)

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

set_tracing_disabled(disabled=True)


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=external_client
)

config = RunConfig(model=model, model_provider=external_client)

class CountryOutput(BaseModel):
    is_country_allowed: bool
    reasoning: str
    country: str

country_agent = Agent(
    name="Country Guardrail check",
    instructions="we only allow to talk about pakistan.do not answer question about any other Country or aspect",
    output_type=CountryOutput,
    model=model,
)

query = "what is the capital of pakistan?"
result = Runner.run_sync(country_agent,query,run_config=config)

# 1st print
print('\n\n',result.final_output)

# Data Return in Dic Format 
print('\n\n',result.final_output.model_dump())

# 2nd print

print(result.final_output.is_country_allowed)
print(result.final_output.reasoning)
print(result.final_output.country)

```
#### Output:
```bash
is_country_allowed=True reasoning='The query is about Pakistan, which is allowed.' country='Pakistan'


 {'is_country_allowed': True, 'reasoning': 'The query is about Pakistan, which is allowed.', 'country': 'Pakistan'} 
True
The query is about Pakistan, which is allowed.
Pakistan
```


## 1. Input guardrails Agent ('sirf pakistan se related Question ka Answer dega ye')
 
#### Note
Input guardrails are intended to run on user input, so an agent's guardrails only run if the agent is the first agent. You might wonder, why is the guardrails property on the agent instead of passed to Runner.run? It's because guardrails tend to be related to the actual Agent - you'd run different guardrails for different agents, so colocating the code is useful for readability.

```bash
import asyncio
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import (
    Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, set_tracing_disabled,
    TResponseInputItem,
    input_guardrail,
    GuardrailFunctionOutput,RunContextWrapper,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered)

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

set_tracing_disabled(disabled=True)


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=external_client
)

config = RunConfig(model=model, model_provider=external_client)

class CountryOutput(BaseModel):
    is_country_allowed: bool
    reasoning: str
    country: str


country_agent = Agent(
    name="Country Guardrail check",
    instructions="we only allow to talk about pakistan.do not answer question about any other Country or aspect",
    output_type=CountryOutput,
    model=model,
)


@input_guardrail
async def guardrail_country_output(
    ctx: RunContextWrapper[None], agent: Agent, output: CountryOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(country_agent, output, context=ctx.context,)
    
    # print('/n/n Guardrail Country Response',result.final_output)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_country_allowed is False,
    )
 
agent = Agent(
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[guardrail_country_output],
)
    

try:
    query = "what is the capital of china?"
    result = Runner.run_sync(agent,query,run_config=config)
    print(result.final_output)


except OutputGuardrailTripwireTriggered:
    print("Output Guardrail Tripped")    
    
except InputGuardrailTripwireTriggered:
    print("Input Guardrail Tripped")
    
```

* jab bhi user query dega to wo input pehly validate hoga. agr user ny pakistan ke elawa koe information pochi to input guardrail grigger 
ho jaega.


## 2. Output guardrails ('sirf pakistan se related Question ka Answer dega ye. output ko validate krke reponse dega')

#### Note
Output guardrails are intended to run on the final agent output, so an agent's guardrails only run if the agent is the last agent. Similar to the input guardrails, we do this because guardrails tend to be related to the actual Agent - you'd run different guardrails for different agents, so colocating the code is useful for readability.

```bash
import asyncio
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import (
    Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, set_tracing_disabled,
    TResponseInputItem,
    input_guardrail,
    output_guardrail,
    GuardrailFunctionOutput,RunContextWrapper,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered)

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

set_tracing_disabled(disabled=True)


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=external_client
)

config = RunConfig(model=model, model_provider=external_client)

class CountryOutput(BaseModel):
    is_country_allowed: bool
    reasoning: str
    country: str


country_agent = Agent(
    name="Country Guardrail check",
    instructions="we only allow to talk about pakistan.do not answer question about any other Country or aspect",
    output_type=CountryOutput,
    model=model,
)


@output_guardrail
async def guardrail_country_output(
    ctx: RunContextWrapper[None], agent: Agent, output: CountryOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(country_agent, output, context=ctx.context,)
    
    # print('/n/n Guardrail Country Response',result.final_output)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
         tripwire_triggered=not result.final_output.is_country_allowed,
    )
 
agent = Agent(
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    output_guardrails=[guardrail_country_output],
)
    
try:
    query = "what is the capital of china?"
    result = Runner.run_sync(agent,query,run_config=config)
    print(result.final_output)


except OutputGuardrailTripwireTriggered:
    print("Output Guardrail Tripped")    
    
except InputGuardrailTripwireTriggered:
    print("Input Guardrail Tripped")
```

## Code Step-by-Step Explanation

### 1. Output Model Define Karna (Pydantic)

```bash
class CountryOutput(BaseModel):
    is_country_allowed: bool
    reasoning: str
    country: str
```
* Agent se aane wala response validate hoga is structure ke against.


### 2. Guard Agent for Country Check
Ye agent sirf Pakistan se related queries allow karta hai. Ye agent CountryOutput type ka result banata hai — jisme batata hai:

* user ka sawal Pakistan ke baare me tha ya nahi
* reason
* kaunsi country mention hui


### 3. Guardrail Function Define Karna (Output Guardrail)
```bash
@output_guardrail
async def guardrail_country_output(
    ctx: RunContextWrapper[None], agent: Agent, output: CountryOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(country_agent, output, context=ctx.context,)
    
    # print('/n/n Guardrail Country Response',result.final_output)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
         tripwire_triggered=not result.final_output.is_country_allowed,
    )
```  
* Ye function output par guardrail lagata hai
* Ye output ko country_agent ko deta hai taake check kare:
    * Kya country allowed hai?
    * Agar False hai → tripwire_triggered=True → block the output 

```bash
Agar is_country_allowed = False → tripwire trigger hoga.
```
* Agar is_country_allowed = False → tripwire trigger hoga.


### 4. Actual Agent (jo user query handle karta hai)
```bash
agent = Agent(
    name="Customer support agent",
    instructions="You are a customer support agent...",
    output_guardrails=[guardrail_country_output],
)
```
* Ye agent user ke queries handle karta hai — lekin uska output guardrail se check hoga. Agar guardrail ke mutabiq output illegal hai, to block ho jayega.

### 5. Run the Agent and Handle Exceptions
```bash
try:
    query = "what is the capital of china?"
    result = Runner.run_sync(agent, query, run_config=config)
    print(result.final_output)
```
* User ka sawal diya gaya hai
* Agent ko Runner.run_sync(...) se run kiya gaya
* Agar country Pakistan nahi hui → guardrail tripwire trigger karega

### 5. Tripwire Exceptions Catch Karna
```bash
except OutputGuardrailTripwireTriggered:
    print("Output Guardrail Tripped")    
except InputGuardrailTripwireTriggered:
    print("Input Guardrail Tripped")
```
* Agar output guardrail ne block kiya (like "China" mention hua) → ye exception trigger hota hai.
