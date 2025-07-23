
Lifecycle hooks ek tarah ke functions/methods hote hain jo automatically agent ya tool ke kisi important stage pe trigger hote hain — jaise start hone se pehle, complete hone ke baad, ya kisi tool ko call karne se pehle/baad.

* Logging kar sakein (jaise: tool kis waqt chala)
* Debug kar sakein (kya agent ne handoff kiya)
* Custom logic daal sakein (e.g., before tool run, validate inputs)


### Types of Hooks:
| Hook Type    | Kya Control Karta Hai         | Use Case Example                      |
| ------------ | ----------------------------- | ------------------------------------- |
| `RunHooks`   | **Global** – sab agents/tools | Har agent ya tool ke start/end pe log |
| `AgentHooks` | **Specific agent** ke liye    | Sirf NutritionAgent ke tool log karo  |


### RunHooksBase
A class that receives callbacks on various lifecycle events in an agent run. Subclass and override the methods you need.
**Bases: Generic[TContext, TAgent]**

#### 1. on_agent_start
Called before the agent is invoked. Called each time the current agent changes.

```bash
on_agent_start(
    context: RunContextWrapper[TContext], agent: TAgent
) -> None
```

#### 2. on_agent_end 
Called when the agent produces a final output.

```bash
on_agent_end(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    output: Any,
) -> None
```

#### 3. on_handoff
Called when a handoff occurs.

```bash
on_handoff(
    context: RunContextWrapper[TContext],
    from_agent: TAgent,
    to_agent: TAgent,
) -> None
```

#### 4. on_tool_end
Called after a tool is invoked.

```bash
on_tool_end(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    tool: Tool,
    result: str,
) -> None
```

### AgentHooksBase
**Bases: Generic[TContext, TAgent]**

A class that receives callbacks on various lifecycle events for a specific agent. You can set this on agent.hooks to receive events for that specific agent.

#### 1. on_start 
Called before the agent is invoked. Called each time the running agent is changed to this agent.

```bash
on_start(
    context: RunContextWrapper[TContext], agent: TAgent
) -> None
```

#### 2. on_end
Called when the agent produces a final output.

```bash
on_end(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    output: Any,
) -> None
```

#### 3. on_handoff
Called when the agent is being handed off to. The source is the agent that is handing off to this agent.

```bash
on_handoff(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    source: TAgent,
) -> None
```

#### 4. on_tool_start
Called before a tool is invoked.

```bash
on_tool_start(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    tool: Tool,
) -> None
```

#### 5. on_tool_end 
Called after a tool is invoked.

```bash
on_tool_end(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    tool: Tool,
    result: str,
) -> None
```

