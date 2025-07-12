
### Health & Wellness Agent
A modular AI assistant built with the OpenAI Agents SDK — designed to help users set goals, plan meals, recommend workouts, schedule check-ins, and track progress, all via real-time CLI interaction.



```bash
pip install openai-agents
```

###  Project Structure 

health_wellness_agent/
│
├── agents/                          # Specialized sub-agents
│   ├── escalation_agent.py          # Handles critical issues escalation
│   ├── injury_support_agent.py      # Advice for injuries or recovery
│   └── nutrition_expert_agent.py    # Nutrition-related queries
│
├── tools/                           # Modular tools for agent assistance
│   ├── goal_analyzer.py             # Analyze and validate goals
│   ├── meal_planner.py              # Generate meal plans
│   ├── scheduler.py                 # Schedule-related tasks
│   ├── tracker.py                   # Progress and activity tracking
│   └── workout_recommender.py       # Suggest workouts
│
├── agent.py                         # Multi-turn agent orchestration logic
├── context.py                       # Manages user/session state context
├── guardrails.py                    # Input/output validation using Pydantic
├── hooks.py                         # Event logging and lifecycle hooks
├── main.py                          # Entrypoint for the app (e.g. Streamlit)
├── .env                             # API keys and environment config
├── README.md                        # Project overview and instructions
