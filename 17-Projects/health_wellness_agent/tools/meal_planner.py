from typing_extensions import TypedDict, Annotated
from typing import List
from agents import function_tool, RunContextWrapper
from pydantic import BaseModel, Field
from context import UserSessionContext


# ────────────────────────────────────────────────────────────────────
# Input / output models
# ────────────────────────────────────────────────────────────────────

class MealPlanInput(BaseModel):
    diet_style: str = Field(
        "balanced",
        examples=["balanced", "vegetarian", "vegan", "keto", "mediterranean"],
        description="Overall dietary preference.",
    )
    calories_per_day: Annotated[int | None, Field(gt=0)] = None


class DailyMeals(TypedDict):
    breakfast: str
    lunch: str
    dinner: str


class MealPlanOutput(TypedDict):
    meal_plan: List[DailyMeals]


# ────────────────────────────────────────────────────────────────────
# Tool implementation
# ────────────────────────────────────────────────────────────────────

@function_tool
async def meal_planner(
    ctx: RunContextWrapper[UserSessionContext],
    input: MealPlanInput,
) -> MealPlanOutput:
    """Generate a stubbed 7-day meal plan."""
    style = input.diet_style.lower()
    cals = input.calories_per_day or 2000

    # Very naive templates — swap with real generator later.
    breakfast = {
        "balanced":      "Oatmeal with berries & almond butter",
        "vegetarian":    "Greek yogurt, banana & honey",
        "vegan":         "Tofu scramble with spinach & toast",
        "keto":          "Avocado, smoked salmon & eggs",
        "mediterranean": "Tomato-feta omelette & whole-grain bread",
    }[style]

    lunch = {
        "balanced":      "Quinoa salad with chicken & veggies",
        "vegetarian":    "Lentil soup & mixed-greens salad",
        "vegan":         "Chickpea bowl with brown rice & tahini",
        "keto":          "Grilled chicken caesar (no croutons)",
        "mediterranean": "Falafel wrap & side tabbouleh",
    }[style]

    dinner = {
        "balanced":      "Baked salmon, sweet potato, broccoli",
        "vegetarian":    "Vegetable stir-fry & tofu",
        "vegan":         "Black-bean chili & avocado",
        "keto":          "Steak, asparagus & cauliflower mash",
        "mediterranean": "Grilled sea-bass, couscous & salad",
    }[style]

    plan: List[DailyMeals] = [
        {"breakfast": breakfast,
         "lunch": lunch,
         "dinner": dinner}
        for _ in range(7)
    ]

    # Persist to session if useful later
    ctx.context.meal_plan = plan
    return {"meal_plan": plan}