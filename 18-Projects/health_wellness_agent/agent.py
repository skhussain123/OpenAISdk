# agent.py

from agents import Agent, handoff
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))

from nutrition_expert_agent import nutrition_expert_agent
from injury_support_agent import injury_support_agent
from escalation_agent import escalation_agent

from goal_analyzer import goal_analyzer
from scheduler import scheduler
from tracker import tracker
from workout_recommender import workout_recommender
from meal_planner import meal_planner


class SeparateAgent:
    def __init__(self, history, query):  # ✅ Constructor added
        self.history = history
        self.query = query
        self.triage_agent = self.build_agent()

    def build_agent(self):
        conversation = "\n".join(
            [f"{msg['role'].capitalize()}: {msg['content']}" for msg in self.history]
        )

        return Agent(
            name="TriageAgent",
            instructions=f"""
You are a helpful health and wellness assistant.

You are allowed to use the full chat history provided below to understand the user's needs, recall facts (like user's name), and maintain context.

{conversation}

Based on the query, decide:
- If it's about diet, meal, or food → hand off to NutritionExpert
- If it's about injury, pain, or recovery → hand off to InjurySupport
- For anything else, either answer directly or hand off to EscalationAgent if needed.

If the user asks something simple (like their name or something from earlier), you can answer directly using the chat history.

Use tools (like goal_analyzer) only when applicable.
""",
            handoffs=[
                handoff(nutrition_expert_agent),
                handoff(injury_support_agent),
                handoff(escalation_agent),
            ],
            tools=[
                goal_analyzer,
                meal_planner,
                scheduler,
                tracker,
                workout_recommender,
            ],
        )
