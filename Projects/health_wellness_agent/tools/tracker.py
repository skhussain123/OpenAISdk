from datetime import datetime
from typing_extensions import TypedDict, Annotated
from agents import function_tool, RunContextWrapper
from pydantic import BaseModel, Field
from context import UserSessionContext


class ProgressInput(BaseModel):
    metric: str = Field(..., description="What you’re reporting e.g. 'weight', 'run_time'")
    value: Annotated[float | str, Field(..., description="Numeric or free-text value")]
    notes: str | None = Field(None, description="Optional comment")


class ProgressOut(TypedDict):
    stored: bool
    log_count: int


@function_tool
async def tracker(
    ctx: RunContextWrapper[UserSessionContext],
    input: ProgressInput,
) -> ProgressOut:
    """Store a progress update in session context."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "metric": input.metric.lower(),
        "value": input.value,
        "notes": input.notes,
    }
    ctx.context.progress_logs.append(log_entry)
    return {"stored": True, "log_count": len(ctx.context.progress_logs)}