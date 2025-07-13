

## Handoffs
Handoffs allow an agent to delegate tasks to another agent. This is particularly useful in scenarios where different agents specialize in distinct areas. For example, a customer support app might have agents that each specifically handle tasks like order status, refunds, FAQs, etc.

Handoffs are represented as tools to the LLM. So if there's a handoff to an agent named Refund Agent, the tool would be called transfer_to_refund_agent.

Ek agent ka kaam kisi doosray agent ya tool ko de dena — jab pehla agent decide kare ke
"ye kaam main nahi kar sakta, ya ye kaam is specific tool/agent ko karna chahiye."


## Creating a handoff
All agents have a handoffs param, which can either take an Agent directly, or a Handoff object that customizes the Handoff.

You can create a handoff using the handoff() function provided by the Agents SDK. This function allows you to specify the agent to hand off to, along with optional overrides and input filters.

```bash
# Urdu agent
urdu_agent = Agent(
    name="Urdu Agent",
    instructions="آپ صرف اردو میں جواب دیتے ہیں۔"
)

# English agent
english_agent = Agent(
    name="English Agent",
    instructions="You only respond in English."
)

# Triage agent with handoff logic
triage_agent = Agent(
    name="Triage Agent",
    instructions="""
If the input is in Urdu or contains Urdu characters, then handoff to the Urdu Agent.
Otherwise, handoff to the English Agent.
""",
    handoffs=[handoff(urdu_agent), handoff(english_agent)],
)
```

## Customizing handoffs via the handoff() function
The handoff() function lets you customize things.

* agent: This is the agent to which things will be handed off.
* tool_name_override: By default, the Handoff.default_tool_name() function is used, which resolves to transfer_to_<agent_name>. You can override this.
* tool_description_override: Override the default tool description from Handoff.default_tool_description()
* on_handoff: A callback function executed when the handoff is invoked. This is useful for things like kicking off some data fetching as soon as you know a handoff is being invoked. This function receives the agent context, and can optionally also receive LLM generated input. The input data is controlled by the input_type param.
* input_type: The type of input expected by the handoff (optional).
* input_filter: This lets you filter the input received by the next agent. See below for more.


#### 1. tool_name_override && tool_description_override

```bash

# Urdu agent
urdu_agent = Agent(
    name="Urdu Agent",
    instructions="آپ صرف اردو میں جواب دیتے ہیں۔"
)


urdu_handoff_obj = handoff(
    agent=urdu_agent,
    tool_name_override="custom_urdu_handoff_tool",
    tool_description_override="This tool hands off the conversation to the Urdu Agent." 
)

# English agent
english_agent = Agent(
    name="English Agent",
    instructions="You only respond in English."
)

english_handoff_obj = handoff(
    agent=english_agent,
    tool_name_override="custom_english_handoff_tool",
    tool_description_override="This tool hands off the conversation to the English Agent." 
)

# Triage agent with handoff logic
triage_agent = Agent(
    name="Triage Agent",
    instructions="""
If the input is in Urdu or contains Urdu characters, then handoff to the Urdu Agent.
Otherwise, handoff to the English Agent.
""",
    handoffs=[urdu_handoff_obj, english_handoff_obj],
)
```


#### 3. on_handoff
A callback function executed when the handoff is invoked. This is useful for things like kicking off some data fetching as soon as you know a handoff is being invoked. This function receives the agent context, and can optionally also receive LLM generated input. The input data is controlled by the input_type param.
```bash
# Urdu agent
urdu_agent = Agent(
    name="Urdu Agent",
    instructions="آپ صرف اردو میں جواب دیتے ہیں۔"
)

def on_handoff_log_urdu(ctx):
    print("Urdu Handoff triggered!")
    

urdu_handoff_obj = handoff(
    agent=urdu_agent,
    on_handoff=on_handoff_log_urdu,
    tool_name_override="custom_urdu_handoff_tool",
    tool_description_override="This tool hands off the conversation to the Urdu Agent." 
)


# English agent
english_agent = Agent(
    name="English Agent",
    instructions="You only respond in English."
)

def on_handoff_log_eng(ctx):
    print("English Handoff triggered!")
    

english_handoff_obj = handoff(
    agent=english_agent,
    on_handoff=on_handoff_log_eng,
    tool_name_override="custom_english_handoff_tool",
    tool_description_override="This tool hands off the conversation to the English Agent."
)

# Triage agent with handoff logic
triage_agent = Agent(
    name="Triage Agent",
    instructions="""
If the input is in Urdu or contains Urdu characters, then handoff to the Urdu Agent.
Otherwise, handoff to the English Agent.
""",
    handoffs=[urdu_handoff_obj, english_handoff_obj],
)
```

#### 3. input_type
input_type batata hai ke LLM jab tool ko call karega to us tool ko kis type ka input dena hai — ye type ho sakta hai:

* str (default string)
* int, float, bool
* dict, list
* Ya koi custom Pydantic model (for structured input)


##### Simple string input
```bash
pip install pydantic
```

##### handoff() me input_type=MessageInput add karo
```bash
#  Define input type (Pydantic model)
class MessageInput(BaseModel):
    message: str

# Define Urdu agent
urdu_agent = Agent(
    name="Urdu Agent",
    instructions="آپ صرف اردو میں جواب دیتے ہیں۔"
)

# on_handoff
def on_handoff_log_urdu(ctx, input):
    print("➡️ Urdu Handoff triggered!")
    print("📥 Urdu input received:", input)

# Customized handoff tool for Urdu
urdu_handoff_obj = handoff(
    agent=urdu_agent,
    on_handoff=on_handoff_log_urdu,
    tool_name_override="custom_urdu_handoff_tool",
    tool_description_override="This tool hands off the conversation to the Urdu Agent.",
    input_type=MessageInput
)

# Define English agent
english_agent = Agent(
    name="English Agent",
    instructions="You only respond in English."
)

# on_handoff
def on_handoff_log_english(ctx, input):
    print("➡️ English Handoff triggered!")
    print("📥 English input received:", input)


# Customized handoff tool for English
english_handoff_obj = handoff(
    agent=english_agent,
    on_handoff=on_handoff_log_english,
    tool_name_override="custom_english_handoff_tool",
    tool_description_override="This tool hands off the conversation to the English Agent.",
    input_type=MessageInput
)

# Define Triage Agent
triage_agent = Agent(
    name="Triage Agent",
    instructions="""
You are a language router agent.

- If the message contains Urdu or Urdu characters like "آپ", "میں", etc., call the `custom_urdu_handoff_tool` with {"message": "<user message>"}.
- If the message is in English, call the `custom_english_handoff_tool` with {"message": "<user message>"}.
- Do NOT respond yourself. Always use one of the tools.
""",
    model=model,
    handoffs=[urdu_handoff_obj, english_handoff_obj],
)
```