from agents import Agent
from pydantic import BaseModel

class AgentResponse(BaseModel):
    response: str
    
    
injury_support_agent = Agent(
    name="InjurySupport",
    instructions="""
You are an injury recovery expert. Help users with injury, pain, or recovery questions.
[AGENT: INJURY]
""",
    # output_type=AgentResponse
)
