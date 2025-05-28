# 1. What is the OpenAI Agents SDK?

The OpenAI Agents SDK is a new framework that enables developers to build and run AI agents that can interact with tools, APIs, and environments in a structured, autonomous way. It provides an interface for creating multi-step, goal-oriented AI behaviors — allowing developers to combine reasoning, memory, and tool usage within a single agent.

### The Agents SDK has a very small set of primitives:

* **Agents,** which are LLMs equipped with instructions and tools
* **Handoffs,** which allow agents to delegate to other agents for specific tasks
* **Guardrails,** which enable the inputs to agents to be validated

In combination with Python, these primitives are powerful enough to express complex relationships between tools and agents, and allow you to build real-world applications without a steep learning curve. In addition, the SDK comes with built-in tracing that lets you visualize and debug your agentic flows, as well as evaluate them and even fine-tune models for your application


## Why use the Agents SDK

1. Enough features to be worth using, but few enough primitives to make it quick to learn.
2. Works great out of the box, but you can customize exactly what happens.

**Here are the main features of the SDK:**

* Agent loop: Built-in agent loop that handles calling tools, sending results to the LLM, and looping until the LLM is done.
* Python-first: Use built-in language features to orchestrate and chain agents, rather than needing to learn new abstractions.
* Handoffs: A powerful feature to coordinate and delegate between multiple agents.
* Guardrails: Run input validations and checks in parallel to your agents, breaking early if the checks fail.
* Function tools: Turn any Python function into a tool, with automatic schema generation and Pydantic-powered validation.
* Tracing: Built-in tracing that lets you visualize, debug and monitor your workflows, as well as use the OpenAI suite of evaluation, fine-tuning and distillation tools.

### Installation
```bash
pip install openai-agents
```

### Hello world example
```bash
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)

# Code within the code,
# Functions calling themselves,
# Infinite loop's dance.

```
--
In Agentic AI, the terms stateful and stateless refer to how an AI agent manages and remembers information over time, especially during interactions or tasks.

### Stateful AI Agents
Definition: A stateful agent remembers previous interactions, decisions, or events. It maintains a "memory" or state during its operation.
Use Case: Useful for multi-step reasoning, long conversations, or task planning.

### Stateless AI Agents

Definition: A stateless agent does not retain memory of previous steps or interactions. Every input is treated independently.
Use Case: Good for simple, single-step tasks.



# 2. Running agents
You can run agents via the Runner class. You have 3 options:

1. Runner.run(), which runs async and returns a RunResult.
2. Runner.run_sync(), which is a sync method and just runs .run() under the hood.
3. Runner.run_streamed(), which runs async and returns a RunResultStreaming. It calls the LLM in streaming mode, and streams those events to you as they are received.


```bash
from agents import Agent, Runner

async def main():
    agent = Agent(name="Assistant", instructions="You are a helpful assistant")

    result = await Runner.run(agent, "Write a haiku about recursion in programming.")
    print(result.final_output)
    # Code within the code,
    # Functions calling themselves,
    # Infinite loop's dance.
```