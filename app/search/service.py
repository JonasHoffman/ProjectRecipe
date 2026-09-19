from sqlalchemy.orm import Session

from app.schemas.recipe import RecipeSearchQuery
from app.search.interpreter import RecipeSearchInterpreter
from app.search.recipe import search_recipes


class RecipeSearchService:

    def __init__(self):
        self.interpreter = RecipeSearchInterpreter()

    def search(
        self,
        text: str,
        db: Session,
    ):
        search_query = self.interpreter.interpret(text)

        return search_recipes(
            db,
            search_query,
        )