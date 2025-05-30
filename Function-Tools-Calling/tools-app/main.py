
import os
import requests
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig
from tavily import TavilyClient



# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
client = TavilyClient("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")



@function_tool
def web_search(query: str) -> str:
    """
    Perform a real-time web search using the Tavily API and return top 3 results.
    """
    try:
        response = client.search(query=query)
        top_results = response.get("results", [])[:3]
        if not top_results:
            return "No results found."
        
        results_text = "\n".join(f"{r.get('title')} - {r.get('url')}" for r in top_results)
        return results_text
    
    except Exception as e:
        return f"Search failed: {str(e)}"
    


# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")




external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# # Defining the Gemini-2.0-flash model for OpenAI-style chat completions
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# # RunConfig object is created which defines the model and the provider
config = RunConfig(
    model=model,
    model_provider=external_client,
)

agent: Agent = Agent(
    name="Assistant", 
    instructions="""
        You are a helpful assistant. If the user asks something that requires real-time data 
        like news, weather, or stock prices — and you don't know the answer — 
        call the `web_search` tool to get it from the internet.
    """,
    model=model,
    tools=[web_search]
    
    )

# # Running the agent in synchronous mode
query = input('Enter Your Query : ')

result = Runner.run_sync(
    agent,
    query,
    run_config=config)

print(result.final_output)