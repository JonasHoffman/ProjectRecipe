from app.database.database import SessionLocal
from app.persistence.recipe import RecipePersistence


data = {
    "name": "Bolo de chocolate",
    "description": "Bolo de chocolate simples e fácil.",
    "preparation_time": 60,
    "servings": 9,
    "instructions": "Misture os ingredientes e asse.",
    "source_name": "Receiteria",
    "source_url": "https://www.receiteria.com.br/",
    "image_url": "https://example.com/bolo.jpg",
    "ingredients": [
        {
            "name": "farinha de trigo",
            "quantity": "2",
            "unit": "xícaras",
            "details": None,
            "group": "Massa",
            "optional": False,
        },
        {
            "name": "açúcar",
            "quantity": "1",
            "unit": "xícara",
            "details": None,
            "group": "Massa",
            "optional": False,
        },
        {
            "name": "chocolate em pó",
            "quantity": "1",
            "unit": "xícara",
            "details": "(ou achocolatado)",
            "group": "Massa",
            "optional": False,
        },
        {
            "name": "granulado",
            "quantity": "200",
            "unit": "gramas",
            "details": None,
            "group": "Cobertura",
            "optional": True,
        },
    ],
}


db = SessionLocal()

try:
    persistence = RecipePersistence(db)

    recipe = persistence.save(data)

    print(f"Receita salva: {recipe.id} - {recipe.name}")

    for item in recipe.ingredients:
        print(
            f"- {item.ingredient.name}: "
            f"{item.quantity} "
            f"{item.unit}"
        )

finally:
    db.close()