from app.ai.client import get_gemini_client
from app.schemas.recipe import RecipeSearchQuery


class RecipeSearchInterpreter:

    def __init__(self):
        self.client = get_gemini_client()

    def interpret(self, text: str) -> RecipeSearchQuery:
        prompt = f"""
Extract recipe search filters from the user's request.

Rules:
- Extract all ingredients explicitly requested by the user.
- Extract the maximum preparation time in minutes if provided.
- Do not invent ingredients.
- If no maximum preparation time is provided, use null.
- Return only data that belongs to the provided schema.

User request:
{text}
"""

        interaction = self.client.interactions.create(
            model="gemini-3.5-flash",
            input=prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": RecipeSearchQuery.model_json_schema(),
            },
        )

        return RecipeSearchQuery.model_validate_json(
            interaction.output_text
        )