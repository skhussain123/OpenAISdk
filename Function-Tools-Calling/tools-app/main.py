
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
api_key_weather = "7b06d00320b7a9bd152efc99b5e44b53"



# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


# @function_tool
# def get_weather(location: str) -> str:
#     """
#     Returns the current weather for a given location.
#     For now, returns a static message to test if the function is being called.
#     """
#     return f"Static response the tool is Calling"


# @function_tool
# def web_live_search(query: str) -> str:
#     """
#     Perform a real-time web search using the Tavily API and return top 3 results.
#     """
#     try:
#         response = client.search(query=query)
#         top_results = response.get("results", [])[:3]
#         if not top_results:
#             return "No results found."
        
#         results_text = "\n".join(f"{r.get('title')} - {r.get('url')}" for r in top_results)
#         return results_text
    
#     except Exception as e:
#         return f"Search failed: {str(e)}"
    
    
@function_tool
def getWeather(city: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key_weather}&units=metric"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        return f"Weather in {city}: {weather}, Temperature: {temp}°C"
    else:
        return f"Failed to get weather for {city}. Status code: {response.status_code}"
        



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


agent = Agent(
    name="Weather Agent",
    instructions=(
        "You're a weather agent. If the user asks for the weather of any specific city, "
        "use the weather tool to give the answer. For anything else, reply: "
        "'I'm just a weather agent, I can only tell you the weather.'"
    ),
    model=model,
    tools=[getWeather]
)


# agent: Agent = Agent(
#     name="Assistant", 
#      instructions="You are a helpful assistant that can search the web using the 'web_live_search' tool. "
#                  "When a user asks a question, check if a real-time search would help, and use the tool if needed.",
#     model=model,
#     tools=[web_live_search]
    
#     )

# # Running the agent in synchronous mode
query = input('Enter Your Query : ')

result = Runner.run_sync(
    agent,
    query,
    run_config=config)

print(result.final_output)