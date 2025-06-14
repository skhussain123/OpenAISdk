from litellm import completion
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")
open_api_key = os.getenv("OPENAI_API_KEY")

# Check if the API key exists
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")


if not open_api_key:
    raise ValueError("open_api_key is not set. Please ensure it is defined in your .env file.")


def gemini():
    response = completion(
        model="gemini/gemini-1.5-flash",
        messages=[{"role": "user", "content": "Hello, how are you?"}],
        api_key=gemini_api_key
    )
    print(response.choices[0].message["content"])


def gemini2():
    response = completion(
        model="gemini/gemini-2.0-flash-exp",
        messages=[{ "content": "Hello, how are you?","role": "user"}],
        api_key=gemini_api_key
    )
    print(response.choices[0].message["content"])   
        
    
def openai():
    response = completion(
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": "Hello, how are you?"}],
        api_key=open_api_key
    )
    print(response.choices[0].message["content"])   
    
     

# Run the function
# gemini()
# openai()
gemini2()
