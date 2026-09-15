from pydantic import BaseModel


class IngredientResponse(BaseModel):

    name: str
    quantity: str | None = None
    unit: str | None = None
    details: str | None = None
    group: str | None = None
    optional: bool = False