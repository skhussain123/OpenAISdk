from agents import RunHooks, Agent
from agents.run import RunContextWrapper

class LoggingRunHooks(RunHooks):
    async def on_start(self, context: RunContextWrapper, agent: Agent):
        print(f"[HOOK] Agent starting: {agent.name}")

    async def on_end(self, context: RunContextWrapper, agent: Agent, output):
        print(f"[HOOK] Agent ended: {agent.name} with output: {output}")

    async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool, tool_input):
        print(f"[HOOK] Tool started: {tool.name} with input: {tool_input}")

    async def on_tool_end(self, context: RunContextWrapper, agent: Agent, tool, result):
        print(f"[HOOK] Tool ended: {tool.name} returned: {result}")

    async def on_handoff(self, context: RunContextWrapper, from_agent: Agent, to_agent: Agent):
        print(f"[HOOK] Handoff from {from_agent.name} to {to_agent.name}")
