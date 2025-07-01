import os
import requests
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel

# Load API key from .env
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Define weather function
@function_tool
def getWeather(city: str) -> str:
    result = requests.get(
        f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}"
    )
    if result.status_code == 200:
        data = result.json()
        return f"The weather in {city} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."
    else:
        return "Sorry, I couldn't fetch the weather data."

# Create agent
agent = Agent(
    name="hello",
    instructions="You are a helpful assistant.",
    model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=gemini_api_key),
    tools=[getWeather],
)

# Run function
def run(message: str) -> str:
    print("Run message:", message)
    result = Runner.run_sync(agent, f"{message}?")
    return result.final_output

# ✅ Add this to actually trigger the run
if __name__ == "__main__":
    user_input = "What's the weather like in Islamabad?"
    
    
    response = run(user_input)
    print("Agent Response:", response)
