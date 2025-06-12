import os
import chainlit as cl
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Optional, Dict 


# Load environment variables from .env file
load_dotenv()

# Get Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini with API key
genai.configure(api_key=gemini_api_key)

# Initialize Gemini model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash"
)


# Decorator to handle OAuth callback from GitHub
@cl.oauth_callback
def oauth_callback(
    provider_id: str,
    token: str, 
    raw_user_data: Dict[str, str],
    default_user: cl.User,
) -> Optional[cl.User]:
    """
    Handle the OAuth callback from GitHub
    Return the user object if authentication is successful, None otherwise
    """

    return default_user 


# Handler for when a new chat session starts
@cl.on_chat_start
async def handle_chat_start():

    cl.user_session.set("history", []) 

    await cl.Message(
        content="Hello! How can I help you today?"
    ).send()


# Handler for incoming chat messages
@cl.on_message
async def handle_message(message: cl.Message):

    history = cl.user_session.get("history")  # Get chat history from session

    history.append(
        {"role": "user", "content": message.content}
    )  # Add user message to history


    # Format chat history for Gemini model
    formatted_history = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"  # Determine message role
        formatted_history.append(
            {"role": role, "parts": [{"text": msg["content"]}]}
        )  # Format message

    response = model.generate_content(formatted_history)

    response_text = (
        response.text if hasattr(response, "text") else ""
    )

    history.append(
        {"role": "assistant", "content": response_text}
    )  
    
    # Add assistant response to history
    cl.user_session.set("history", history)

    await cl.Message(content=response_text).send()