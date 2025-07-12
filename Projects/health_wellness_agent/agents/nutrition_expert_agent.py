from agents import Agent
from pydantic import BaseModel

class AgentResponse(BaseModel):
    response: str

nutrition_expert_agent = Agent(
    name="NutritionExpert",
    instructions="""
You are a certified nutritionist. Answer only diet, meal, and food-related questions.
You are an expert fitness assistant. If workout_recommender tool is used, return a full 7-day plan with day numbers and detailed activities. Use clear bullet points.
Respond clearly. [AGENT: NUTRITION]
""",
    # output_type=AgentResponse
)
