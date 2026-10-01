from app.ai.client import get_gemini_client
from app.schemas.recipe import RecipeSelection


class RecipeSelector:
    def __init__(self):
        self.client = get_gemini_client()

    def select(
        self,
        user_query: str,
        recipes: list[dict],
    ) -> RecipeSelection:
        recipe_ids = [
            recipe["id"]
            for recipe in recipes
        ]

        prompt = f"""
Select one recipe based on the user's request.

Rules:
- Select only one recipe.
- The selected recipe ID must be one of the provided recipe IDs.
- Never invent a recipe ID.
- Use the recipe information to understand the user's preference.
- If the user refers to "first", "second", etc., use the position in the provided list.
- Return only data that belongs to the provided schema.

User request:
{user_query}

Available recipes:
{recipes}
"""

        interaction = self.client.interactions.create(
            model="gemini-3.5-flash",
            input=prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": RecipeSelection.model_json_schema(),
            },
        )

        selection = RecipeSelection.model_validate_json(
            interaction.output_text
        )

        if selection.recipe_id not in recipe_ids:
            raise ValueError(
                "Gemini selected an unavailable recipe."
            )

        return selection