from agents import Agent, FileSearchTool, Runner, WebSearchTool

agent = Agent(
    name="Assistant",
    tools=[
        WebSearchTool(),
        FileSearchTool(
            max_num_results=3,
            # vector_store_ids=["VECTOR_STORE_ID"],
            vector_store_ids=["vs_6813268d82a081919782a0990f3a68f9"],

        ),
    ],
)
result =  Runner.run_sync(agent, "Current Pakistan India News")
print(result.final_output)
