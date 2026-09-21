from app.ai.client import get_gemini_client
from app.schemas.recipe import RecipeRecommendationResponse


class RecipeRecommender:
    def __init__(self):
        self.client = get_gemini_client()

    def recommend(
        self,
        user_query: str,
        recipes: list[dict],
    ) -> RecipeRecommendationResponse:
        prompt = f"""
Recommend recipes based only on the recipes provided below.

Rules:
- Recommend only recipes from the provided list.
- Never invent recipes.
- Never invent recipe IDs.
- Use the user's request to explain why each recommendation is relevant.
- Keep the response concise.
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
                "schema": RecipeRecommendationResponse.model_json_schema(),
            },
        )

        return RecipeRecommendationResponse.model_validate_json(
            interaction.output_text
        )