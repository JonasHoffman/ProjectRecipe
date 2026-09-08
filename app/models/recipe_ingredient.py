from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column,relationship

from app.database.database import Base


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id"),
    )

    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id"),
    )

    quantity: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    recipe: Mapped["Recipe"] = relationship(
        back_populates="ingredients",
    )

    ingredient: Mapped["Ingredient"] = relationship(
        back_populates="recipes",
    )