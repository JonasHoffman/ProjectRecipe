from app.database.database import SessionLocal
from app.normalizer.recipe import RecipeNormalizer
from app.persistence.recipe import RecipePersistence


raw_data = {
    "title": "  Bolo de chocolate fácil e molhadinho ",
    "preparation_time": "1 hora",
    "servings": "9 porções",
    "steps": [
        {
            "group": "Massa",
            "items": [
                "Misture os ingredientes.",
                "Coloque em uma forma.",
            ],
        },
        {
            "group": "Cobertura",
            "items": [
                "Prepare a cobertura.",
                "Cubra o bolo.",
            ],
        },
    ],
    "ingredients": [
        {
            "group": "Massa",
            "items": [
                "2 xícaras de farinha de trigo",
                "1 xícara de açúcar",
                "1 xícara de chocolate em pó",
            ],
        },
        {
            "group": "Cobertura",
            "items": [
                "200 gramas de granulado",
            ],
        },
    ],
    "source_name": "Receiteria",
    "source_url": "https://www.receiteria.com.br/",
    "image_url": "https://example.com/bolo.jpg",
}


normalizer = RecipeNormalizer()

normalized_data = normalizer.normalize(
    raw_data,
    raw_data["source_name"],
    raw_data["source_url"],
)

db = SessionLocal()

try:
    persistence = RecipePersistence(db)

    recipe = persistence.save(normalized_data)

    print(f"Recipe saved: {recipe.id} - {recipe.name}")

    for item in recipe.ingredients:
        print(
            f"- {item.ingredient.name}: "
            f"{item.quantity} "
            f"{item.unit}"
        )

finally:
    db.close()