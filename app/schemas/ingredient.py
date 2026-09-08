from pydantic import BaseModel


class IngredientResponse(BaseModel):
    name: str
    quantity: str | None = None