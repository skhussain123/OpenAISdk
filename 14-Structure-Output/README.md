

## What is Structured outputs
Structured outputs refer to responses from a language model that follow a specific format or schema, like JSON, key-value pairs, or function arguments — instead of plain free-form text.v


### 1. Data Return in Dictionary Format
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


### 2. Using dataclasses
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

from dataclasses import dataclass

@dataclass
class dataformat:
    is_country_allowed: bool
    reasoning:str
    country : str

country_agent = Agent(
    name="Country Guardrail check",
    instructions="we only allow to talk about pakistan.do not answer question about any other Country or aspect",
    output_type=dataformat,
    model=model,
)

query = "what is the capital of pakistan?"
result = Runner.run_sync(country_agent,query,run_config=config)

# 1st print
print('\n\n',result.final_output)

# 2nd print

print(result.final_output.is_country_allowed)
print(result.final_output.reasoning)
print(result.final_output.country)
```