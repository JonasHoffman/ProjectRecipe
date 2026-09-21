import unicodedata

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.ingredient import Ingredient
from app.models.recipe import Recipe
from app.models.recipe_ingredient import RecipeIngredient
from app.schemas.recipe import RecipeSearchQuery


def remove_accents(text: str) -> str:
    normalized = unicodedata.normalize(
        "NFD",
        text,
    )

    return "".join(
        character
        for character in normalized
        if unicodedata.category(character) != "Mn"
    )


def search_recipes(
    db: Session,
    search_query: RecipeSearchQuery,
):
    query = db.query(Recipe)

    for ingredient in search_query.ingredients:
        normalized_ingredient = remove_accents(
            ingredient
        )

        query = query.filter(
            Recipe.ingredients.any(
                RecipeIngredient.ingredient.has(
                    func.unaccent(
                        Ingredient.name
                    ).ilike(
                        f"%{normalized_ingredient}%"
                    )
                )
            )
        )

    if search_query.max_preparation_time is not None:
        query = query.filter(
            Recipe.preparation_time
            <= search_query.max_preparation_time
        )

    return query.all()