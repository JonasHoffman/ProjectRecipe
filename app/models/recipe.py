from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
 
from app.database.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    preparation_time: Mapped[int]
    servings: Mapped[int]

    instructions: Mapped[str] = mapped_column(Text)
    source_name: Mapped[str] = mapped_column(String(100))
    source_url: Mapped[str] = mapped_column(String(500))
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan",
    )