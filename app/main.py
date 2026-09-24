from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from app.search.recipe import search_recipes
from app.ai.selector import RecipeSelector
from app.database.database import SessionLocal
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate, RecipeResponse,RecipeSearchQuery,RecipeSearchResult,RecipeRecommendationResponse,RecipeSelection,RecipeSelectionRequest
from app.models.ingredient import Ingredient
from app.models.recipe_ingredient import RecipeIngredient
from app.search.service import RecipeSearchService
from app.ai.recommender import RecipeRecommender
from app.schemas.telegram import TelegramUpdate
from app.integrations.telegram.bot import TelegramBot

app = FastAPI(
    title="Recipe AI",
    description="Sistema inteligente de recomendação de receitas",
    version="0.1.0",
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/recipes/search", response_model=list[RecipeResponse])
def search_recipe_endpoint(
    query: str,
    db: Session = Depends(get_db),
):
    search_query = RecipeSearchQuery(
        ingredients=[query]
    )

    recipes = search_recipes(
        db,
        search_query,
    )

    return [
        {
            "id": recipe.id,
            "name": recipe.name,
            "description": recipe.description,
            "preparation_time": recipe.preparation_time,
            "servings": recipe.servings,
            "instructions": recipe.instructions,
            "source_name": recipe.source_name,
            "source_url": recipe.source_url,
            "image_url": recipe.image_url,
            "ingredients": [
                {
                    "name": item.ingredient.name,
                    "quantity": item.quantity,
                    "unit": item.unit,
                    "details": item.details,
                    "group": item.group,
                    "optional": item.optional,
                }
                for item in recipe.ingredients
            ],
        }
        for recipe in recipes
    
    ]

@app.get(
    "/recipes",
    response_model=list[RecipeResponse],
)
def list_recipes(
    ingredient: str | None = None,
    max_preparation_time: int | None = None,
    db: Session = Depends(get_db),
):
    ingredients = []

    if ingredient:
        ingredients = [
            item.strip()
            for item in ingredient.split(",")
            if item.strip()
        ]

    search_query = RecipeSearchQuery(
        ingredients=ingredients,
        max_preparation_time=max_preparation_time,
    )

    recipes = search_recipes(
        db,
        search_query,
    )

    return [
        {
            "id": recipe.id,
            "name": recipe.name,
            "description": recipe.description,
            "preparation_time": recipe.preparation_time,
            "servings": recipe.servings,
            "instructions": recipe.instructions,
            "source_name": recipe.source_name,
            "source_url": recipe.source_url,
            "image_url": recipe.image_url,
            "ingredients": [
                {
                    "name": item.ingredient.name,
                    "quantity": item.quantity,
                    "unit": item.unit,
                    "details": item.details,
                    "group": item.group,
                    "optional": item.optional,
                }
                for item in recipe.ingredients
            ],
        }
        for recipe in recipes
    ]

@app.get(
    "/recipes/natural-search",
    response_model=list[RecipeSearchResult],
)
def natural_search_recipes(
    query: str,
    db: Session = Depends(get_db),
):
    service = RecipeSearchService()

    recipes = service.search(
        query,
        db,
    )

    return recipes

@app.get(
    "/recipes/recommend",
    response_model=RecipeRecommendationResponse,
)
def recommend_recipes(
    query: str,
    db: Session = Depends(get_db),
):
    service = RecipeSearchService()

    recipes = service.search(
        query,
        db,
    )

    recipe_data = [
        {
            "id": recipe.id,
            "name": recipe.name,
            "description": recipe.description,
            "preparation_time": recipe.preparation_time,
            "servings": recipe.servings,
        }
        for recipe in recipes
    ]

    recommender = RecipeRecommender()

    return recommender.recommend(
        query,
        recipe_data,
    )
@app.post(
    "/recipes/select",
    response_model=RecipeResponse,
)
def select_recipe(
    selection: RecipeSelectionRequest,
    db: Session = Depends(get_db),
):
    selector = RecipeSelector()

    result = selector.select(
        selection.query,
        selection.recipe_ids,
    )

    recipe = (
        db.query(Recipe)
        .filter(Recipe.id == result.recipe_id)
        .first()
    )

    if not recipe:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found",
        )

    return {
        "id": recipe.id,
        "name": recipe.name,
        "description": recipe.description,
        "preparation_time": recipe.preparation_time,
        "servings": recipe.servings,
        "instructions": recipe.instructions,
        "source_name": recipe.source_name,
        "source_url": recipe.source_url,
        "image_url": recipe.image_url,
        "ingredients": [
            {
                "name": item.ingredient.name,
                "quantity": item.quantity,
                "unit": item.unit,
                "details": item.details,
                "group": item.group,
                "optional": item.optional,
            }
            for item in recipe.ingredients
        ],
    }

@app.get("/recipes/{recipe_id}", response_model=RecipeResponse)
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if not recipe:
        raise HTTPException(
            status_code=404,
            detail="Receita não encontrada.",
        )

    return {
        "id": recipe.id,
        "name": recipe.name,
        "description": recipe.description,
        "preparation_time": recipe.preparation_time,
        "servings": recipe.servings,
        "instructions": recipe.instructions,
        "source_name": recipe.source_name,
        "source_url": recipe.source_url,
        "image_url": recipe.image_url,
        "ingredients": [
            {
                "name": item.ingredient.name,
                "quantity": item.quantity,
                "unit": item.unit,
                "details": item.details,
                "group": item.group,
                "optional": item.optional,
            }
            for item in recipe.ingredients
        ],
    }

@app.post("/recipes", response_model=RecipeResponse)
def create_recipe(
    recipe_data: RecipeCreate,
    db: Session = Depends(get_db),
):
    recipe = Recipe(
        name=recipe_data.name,
        description=recipe_data.description,
        preparation_time=recipe_data.preparation_time,
        servings=recipe_data.servings,
        instructions=recipe_data.instructions,
        source_name=recipe_data.source_name,
        source_url=recipe_data.source_url,
        image_url=recipe_data.image_url,
    )

    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    return recipe



@app.post("/telegram/webhook")
def telegram_webhook(
    update: TelegramUpdate,
    db: Session = Depends(get_db),
):
    if not update.message:
        return {
            "ok": True,
        }

    if not update.message.text:
        return {
            "ok": True,
        }

    bot = TelegramBot()

    bot.send_message(
        chat_id=update.message.chat.id,
        text=f"You said: {update.message.text}",
    )

    return {
        "ok": True,
    }




