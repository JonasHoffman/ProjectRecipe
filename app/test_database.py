from app.database.database import SessionLocal
from app.models.recipe import Recipe


db = SessionLocal()

try:
    recipe = db.query(Recipe).filter_by(name="Frango cremoso").first()

    if not recipe:
        print("Receita não encontrada.")
    else:
        print(f"Receita: {recipe.name}")

        for item in recipe.ingredients:
            print(
                f"- {item.ingredient.name}: {item.quantity}"
            )

finally:
    db.close()