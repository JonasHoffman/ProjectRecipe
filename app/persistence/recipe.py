from sqlalchemy.orm import Session

from app.models.ingredient import Ingredient
from app.models.recipe import Recipe
from app.models.recipe_ingredient import RecipeIngredient


class RecipePersistence:

    def __init__(self, db: Session):
        self.db = db

    def save(self, data: dict) -> Recipe:
        recipe = Recipe(
            name=data["name"],
            description=data.get("description"),
            preparation_time=data.get("preparation_time"),
            servings=data.get("servings"),
            instructions=data["instructions"],
            source_name=data["source_name"],
            source_url=data["source_url"],
            image_url=data.get("image_url"),
        )

        self.db.add(recipe)

        for item in data.get("ingredients", []):
            ingredient = self._get_or_create_ingredient(
                item["name"]
            )

            recipe_ingredient = RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient,
                quantity=item.get("quantity"),
                unit=item.get("unit"),
                details=item.get("details"),
                group=item.get("group"),
                optional=item.get("optional", False),
            )

            self.db.add(recipe_ingredient)

        self.db.commit()
        self.db.refresh(recipe)

        return recipe

    def _get_or_create_ingredient(
        self,
        name: str,
    ) -> Ingredient:

        ingredient = (
            self.db.query(Ingredient)
            .filter(Ingredient.name == name)
            .first()
        )

        if ingredient:
            return ingredient

        ingredient = Ingredient(name=name)

        self.db.add(ingredient)
        self.db.flush()

        return ingredient