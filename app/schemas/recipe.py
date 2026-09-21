from pydantic import BaseModel,ConfigDict,Field
from app.schemas.ingredient import IngredientResponse
from sqlalchemy.orm import Mapped



class RecipeCreate(BaseModel):

    name: str
    description: str | None = None
    preparation_time: int | None = None
    servings: int | None = None
    instructions: str
    source_name: str
    source_url: str
    image_url: str | None = None


class RecipeResponse(RecipeCreate):
    id: int
    ingredients: list[IngredientResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

class RecipeSearchQuery(BaseModel):
    ingredients: list[str] = Field(default_factory=list)
    max_preparation_time: int | None = None

class RecipeSearchResult(BaseModel):
    id: int
    name: str
    description: str | None = None
    preparation_time: int | None = None
    servings: int | None = None
    image_url: str | None = None

    model_config = ConfigDict(from_attributes=True)

class RecipeRecommendation(BaseModel):
    recipe_id: int
    reason: str


class RecipeRecommendationResponse(BaseModel):
    message: str
    recommendations: list[RecipeRecommendation]