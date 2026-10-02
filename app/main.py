from fastapi import Depends, FastAPI, HTTPException,BackgroundTasks
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
from google.genai.errors import APIError
from app.audio.transcriber import SpeechToText


app = FastAPI(
    title="Recipe AI",
    description="Sistema inteligente de recomendação de receitas",
    version="0.1.0",
)

telegram_recipe_options = {}

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

def format_recipe_for_telegram(recipe: Recipe) -> str:
    lines = [
        f"🍳 {recipe.name}",
        "",
    ]

    if recipe.description:
        lines.append(recipe.description)
        lines.append("")

    if recipe.preparation_time is not None:
        lines.append(
            f"⏱ Tempo de preparo: "
            f"{recipe.preparation_time} minutos"
        )

    if recipe.servings is not None:
        lines.append(
            f"🍽 Porções: {recipe.servings}"
        )

    lines.append("")
    lines.append("🥕 Ingredientes:")
    lines.append("")

    for item in recipe.ingredients:
        quantity = item.quantity or ""
        unit = item.unit or ""
        name = item.ingredient.name
        details = item.details or ""

        amount = " ".join(
            part
            for part in [quantity, unit]
            if part
        )

        ingredient_parts = [
            part
            for part in [amount, name, details]
            if part
        ]

        ingredient = " ".join(ingredient_parts)

        lines.append(
            f"   • {ingredient}"
        )

    lines.append("")
    lines.append("👨‍🍳 Modo de preparo:")
    lines.append("")

    instructions = recipe.instructions.strip()

    steps = [
        step.strip()
        for step in instructions.split("\n")
        if step.strip()
    ]

    for index, step in enumerate(steps, start=1):
        lines.append(
            f"   {index}. {step}"
        )
        lines.append("")

    return "\n".join(lines).strip()

def get_recipe_position(text: str) -> int | None:
    text = text.lower()

    positions = {
        "primeira": 1,
        "primeiro": 1,
        "segunda": 2,
        "segundo": 2,
        "terceira": 3,
        "terceiro": 3,
        "quarta": 4,
        "quarto": 4,
        "quinta": 5,
        "quinto": 5,
        "first": 1,
        "second": 2,
        "third": 3,
        "fourth": 4,
        "fifth": 5,
    }

    for word, position in positions.items():
        if word in text:
            return position

    if "última" in text or "último" in text:
        return -1

    if "ultima" in text or "ultimo" in text:
        return -1

    if "last" in text:
        return -1

    return None

def process_telegram_message(update: TelegramUpdate):
    db = SessionLocal()

    try:
        message = update.message

        if not message:
            return

        chat_id = message.chat.id
        bot = TelegramBot()

        if message.voice:
            print("VOICE RECEIVED")
            print("MESSAGE ID:", message.message_id)
            print("file_id:", message.voice.file_id)

            file_info = bot.get_file(
                message.voice.file_id
            )

            print("file_info:", file_info)

            file_path = file_info["result"]["file_path"]

            audio_path = "voice.oga"

            bot.download_file(
                file_path,
                audio_path,
            )

            transcriber = SpeechToText()

            transcription = transcriber.transcribe(
                audio_path
            )

            print("TRANSCRIPTION:")
            print(transcription)

            return

        if not message.text:
            return

        user_query = message.text.strip()

        if user_query.lower() == "/start":
            bot.send_message(
                chat_id=chat_id,
                text=(
                    "👋 Olá! Eu sou o Recipe AI.\n\n"
                    "Posso ajudar você a encontrar receitas "
                    "com base no que está procurando.\n\n"
                    "Por exemplo:\n"
                    "• Quero uma receita com frango\n"
                    "• Quero uma receita com chocolate\n"
                    "• Quero uma receita com frango em até 30 minutos\n\n"
                    "Depois que eu encontrar algumas opções, "
                    "você pode escolher dizendo:\n"
                    '"quero a primeira" ou "quero a segunda".\n\n'
                    "Você também pode fazer uma escolha por característica, "
                    'como "quero a mais rápida".'
                ),
            )
            return

        if user_query.lower() == "/help":
            bot.send_message(
                chat_id=chat_id,
                text=(
                    "🤖 Como usar o Recipe AI\n\n"
                    "Você pode pedir receitas usando linguagem natural.\n\n"
                    "Exemplos:\n"
                    "• Quero uma receita com frango\n"
                    "• Quero algo com chocolate\n"
                    "• Quero uma receita com carne em até 30 minutos\n\n"
                    "Depois que eu mostrar as opções, "
                    "você pode escolher uma delas:\n"
                    '• "quero a primeira"\n'
                    '• "quero a segunda"\n'
                    '• "quero a terceira"\n'
                    '• "quero a mais rápida"\n'
                    '• "quero a que leva menos tempo"\n\n'
                    "Comandos disponíveis:\n"
                    "/start - iniciar o bot\n"
                    "/help - mostrar esta ajuda\n"
                    "/reset - limpar a seleção atual"
                ),
            )
            return

        if user_query.lower() == "/reset":
            telegram_recipe_options.pop(
                chat_id,
                None,
            )

            bot.send_message(
                chat_id=chat_id,
                text=(
                    "🔄 Sua seleção foi limpa.\n\n"
                    "Você pode fazer uma nova busca "
                    "quando quiser."
                ),
            )
            return

        recipe_ids = telegram_recipe_options.get(chat_id)

        recipe_position = get_recipe_position(
            user_query
        )

        # Deterministic selection
        if recipe_ids and recipe_position is not None:
            if recipe_position == -1:
                recipe_id = recipe_ids[-1]
            else:
                try:
                    recipe_id = recipe_ids[
                        recipe_position - 1
                    ]
                except IndexError:
                    bot.send_message(
                        chat_id=chat_id,
                        text=(
                            "Não existe uma receita nessa posição. "
                            "Escolha uma das opções que enviei."
                        ),
                    )
                    return

            recipe = (
                db.query(Recipe)
                .filter(Recipe.id == recipe_id)
                .first()
            )

            if not recipe:
                bot.send_message(
                    chat_id=chat_id,
                    text="Não encontrei a receita selecionada.",
                )
                return

            telegram_recipe_options.pop(
                chat_id,
                None,
            )

            bot.send_message(
                chat_id=chat_id,
                text=format_recipe_for_telegram(recipe),
            )

            return

        # Semantic selection
        if recipe_ids:
            available_recipes = (
                db.query(Recipe)
                .filter(Recipe.id.in_(recipe_ids))
                .all()
            )

            if not available_recipes:
                telegram_recipe_options.pop(
                    chat_id,
                    None,
                )

                bot.send_message(
                    chat_id=chat_id,
                    text=(
                        "As opções anteriores não estão mais disponíveis. "
                        "Faça uma nova busca."
                    ),
                )
                return

            recipe_data = [
                {
                    "id": recipe.id,
                    "name": recipe.name,
                    "description": recipe.description,
                    "preparation_time": recipe.preparation_time,
                    "servings": recipe.servings,
                }
                for recipe in available_recipes
            ]

            selector = RecipeSelector()

            try:
                selection = selector.select(
                    user_query,
                    recipe_data,
                )
            except APIError as error:
                if error.code == 429:
                    bot.send_message(
                        chat_id=chat_id,
                        text=(
                            "⚠️ O serviço de IA atingiu o limite de uso "
                            "disponível no momento.\n\n"
                            "Tente novamente mais tarde."
                        ),
                    )
                    return

                raise

            except ValueError:
                bot.send_message(
                    chat_id=chat_id,
                    text=(
                        "Não consegui identificar uma receita "
                        "com base no seu pedido."
                    ),
                )
                return

            recipe = (
                db.query(Recipe)
                .filter(
                    Recipe.id == selection.recipe_id
                )
                .first()
            )

            if not recipe:
                bot.send_message(
                    chat_id=chat_id,
                    text="Não encontrei a receita selecionada.",
                )
                return

            telegram_recipe_options.pop(
                chat_id,
                None,
            )

            bot.send_message(
                chat_id=chat_id,
                text=format_recipe_for_telegram(recipe),
            )

            return

        # New recipe search
        service = RecipeSearchService()

        try:
            recipes = service.search(
                user_query,
                db,
            )
        except APIError as error:
            if error.code == 429:
                bot.send_message(
                    chat_id=chat_id,
                    text=(
                        "⚠️ O serviço de IA atingiu o limite de uso "
                        "disponível no momento.\n\n"
                        "Tente novamente mais tarde."
                    ),
                )
                return

            raise

        if not recipes:
            bot.send_message(
                chat_id=chat_id,
                text=(
                    "Não encontrei receitas para esse pedido. "
                    "Tente pedir outra combinação de ingredientes."
                ),
            )
            return

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

        try:
            recommendation = recommender.recommend(
                user_query,
                recipe_data,
            )
        except APIError as error:
            if error.code == 429:
                bot.send_message(
                    chat_id=chat_id,
                    text=(
                        "⚠️ O serviço de IA atingiu o limite de uso "
                        "disponível no momento.\n\n"
                        "Tente novamente mais tarde."
                    ),
                )
                return

            raise

        telegram_recipe_options[chat_id] = [
            item.recipe_id
            for item in recommendation.recommendations
        ]

        recipes_by_id = {
            recipe.id: recipe
            for recipe in recipes
        }

        for index, item in enumerate(
            recommendation.recommendations,
            start=1,
        ):
            recipe = recipes_by_id.get(item.recipe_id)

            if not recipe:
                continue

            caption_lines = [
                f"{index}. {recipe.name}",
                "",
            ]

            if recipe.description:
                caption_lines.append(
                    recipe.description
                )
                caption_lines.append("")

            caption_lines.append(
                f"💡 {item.reason}"
            )

            if recipe.preparation_time is not None:
                caption_lines.append(
                    f"⏱ Tempo de preparo: "
                    f"{recipe.preparation_time} minutos"
                )

            if recipe.servings is not None:
                caption_lines.append(
                    f"🍽 Porções: {recipe.servings}"
                )

            caption = "\n".join(caption_lines)

            if recipe.image_url:
                bot.send_photo(
                    chat_id=chat_id,
                    photo=recipe.image_url,
                    caption=caption,
                )
            else:
                bot.send_message(
                    chat_id=chat_id,
                    text=caption,
                )

        bot.send_message(
            chat_id=chat_id,
            text=(
                "Qual você gostaria de preparar?\n\n"
                "Você pode escolher pelo número ou "
                "por uma característica.\n\n"
                'Exemplo: "quero a segunda" ou '
                '"quero a mais rápida".'
            ),
        )

    finally:
        db.close()

@app.post("/telegram/webhook")
def telegram_webhook(
    update: TelegramUpdate,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(
        process_telegram_message,
        update,
    )

    return {
        "ok": True,
    }



