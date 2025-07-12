
from typing_extensions import TypedDict
from pydantic import BaseModel, Field, field_validator
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, handoff, function_tool

# --- Inline Goal Analyzer Tool ---
class GoalInput(BaseModel):
    quantity: float = Field(..., gt=0, description="Goal amount (e.g. 5)")
    metric: str = Field(..., description="Measurement unit (e.g. kg)")
    duration: str = Field(..., description="Time frame (e.g. '3 months')")

    @field_validator("metric")
    def normalize_metric(cls, v):
        return v.strip().lower()

class GoalAnalyzerOut(TypedDict):
    parsed_goal: dict

@function_tool
async def goal_analyzer(ctx, input: GoalInput) -> GoalAnalyzerOut:
    """
    Analyze user-written goal and store in session.
    Example: 'lose 5 kg in 3 months'
    """
    parsed = input.model_dump()
    ctx.context.goal = parsed
    return {"parsed_goal": parsed}
