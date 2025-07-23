from agents import Agent
from pydantic import BaseModel

class AgentResponse(BaseModel):
    response: str
    
escalation_agent = Agent(
    name="EscalationAgent",
    instructions="""
You are a general fallback health advisor. If a question doesn't fit nutrition or injury,
handle it with basic wellness advice. [AGENT: ESCALATION]
""",
# output_type=AgentResponse 
)
