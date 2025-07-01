

Interestingly, you can turn other agents into tools. This allows one agent to call another for assistance without fully handing off control. The orchestrator agent uses the other agents as a tool, depending on the user’s request, while retaining oversight.

The as_tool method in OpenAI's Agents SDK allows you to transform an Agent instance into a callable tool that other agents can utilize. This feature facilitates the creation of modular and interactive AI systems where agents can delegate tasks among themselves.

#### This is different from handoffs in two ways:

* In handoffs, the new agent receives the conversation history. In this tool, the new agent receives generated input.
* In handoffs, the new agent takes over the conversation. In this tool, the new agent is called as a tool, and the conversation is continued by the original agent.

### Key Concepts:
1. Agents: Autonomous entities equipped with instructions and tools to perform specific tasks.
2. Tools: Functions or capabilities that agents can invoke to accomplish tasks.
3. Handoffs: Mechanisms enabling agents to delegate tasks to other agents.


##### Using the as_tool Method:
o utilize the as_tool method, you can follow these steps:
 
##### 1. Define Individual Agents:
Create agents with specific roles and instructions.
```bash
from agents import Agent, Runner

# Define a shopping assistant agent
shopping_agent = Agent(
    name="Shopping Assistant",
    instructions="You assist users in finding products and making purchase decisions."
)

# Define a support agent
support_agent = Agent(
    name="Support Agent",
    instructions="You help users with post-purchase support and returns."
)
```
##### 2. Convert Agents into Tools:
Use the as_tool method to make each agent callable by other agents.
```bash
# Convert agents into tools
shopping_tool = shopping_agent.as_tool()
support_tool = support_agent.as_tool()
```

##### 3. Create a Triage Agent:
Develop an agent responsible for routing user queries to the appropriate agent tool.
```bash
# Define a triage agent that delegates tasks
triage_agent = Agent(
    name="Triage Agent",
    instructions="You route user queries to the appropriate department.",
    tools=[shopping_tool, support_tool]
)
```

##### Run the Triage Agent:
Execute the triage agent with a user query to see it in action.
```bash
# Run the triage agent with a sample input
result = Runner.run_sync(triage_agent, "I need help with a recent purchase.")
print(result.final_output)
```

#### Complete Example in uv Project

