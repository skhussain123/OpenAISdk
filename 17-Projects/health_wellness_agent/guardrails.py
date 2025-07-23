from pydantic import BaseModel
from agents import input_guardrail,output_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from agents import Agent, Runner, function_tool

# input guardrail to check if the input is related to health or wellness
class HealthGuardrailOutput(BaseModel):
    is_invalid: bool
    reason: str

# Guardrail checker agent
guardrail_checker_agent = Agent(
    name="Guardrail Checker",
    instructions="Check if the user's input is unrelated to health or wellness.",
    output_type=HealthGuardrailOutput,
)

@input_guardrail
async def health_input_guardrail(ctx, agent, input):
    result = await Runner.run(guardrail_checker_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_invalid
    )

# output guardrail to ensure no sensitive data is leaked
class AgentResponse(BaseModel):
    response: str

class OutputCheck(BaseModel):
    reasoning: str
    is_math_or_invalid: bool


output_guardrail_checker = Agent(
    name="Output Checker",
    instructions="""
Check if the agent's output contains math help, unrelated information (e.g. programming, code, or assignment help).
If yes, set is_math_or_invalid = true.
Otherwise, set is_math_or_invalid = false.
""",
    output_type=OutputCheck,
)

@output_guardrail
async def health_output_guardrail(ctx, agent, output: AgentResponse):
    result = await Runner.run(output_guardrail_checker, output.response, context=ctx.context)
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_or_invalid
    )