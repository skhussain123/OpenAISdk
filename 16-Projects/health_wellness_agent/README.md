
# Health & Wellness Agent 🤖💪

An AI-powered modular health assistant built using OpenAI Agents SDK. This system consists of specialized sub-agents and tools that collaboratively help users achieve their fitness, nutrition, and wellness goals.

---

## 🚀 Features

- ✅ Multi-turn intelligent agent conversations
- 🍽️ Meal planning & nutrition advice
- 🏃 Workout recommendations
- 🎯 Goal analysis and tracking
- 📅 Scheduling assistance
- 🛡️ Guardrails for safe and valid user input
- ⚕️ Escalation for injury or expert help

---
### Installations
```bash
pip install openai-agents
```

###  Project Structure 

```bash
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
```
