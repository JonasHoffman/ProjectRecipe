from app.scraper.http_client import fetch_page
from app.scraper.tudogostoso.parser import TudoGostosoParser
from app.normalizer.recipe import RecipeNormalizer
from app.persistence.recipe import RecipePersistence
from app.database.database import SessionLocal


URL = "https://www.tudogostoso.com.br/receita/23-bolo-de-cenoura.html"


def main():
    html = fetch_page(URL)

    parser = TudoGostosoParser()
    raw_data = parser.parse(html)

    print(f"Scraped recipe: {raw_data['title']}")

    normalizer = RecipeNormalizer()

    normalized_data = normalizer.normalize(
        raw_data,
        "TudoGostoso",
        URL,
    )

    print(f"Normalized recipe: {normalized_data['name']}")
    print(
        f"Ingredients found: "
        f"{len(normalized_data['ingredients'])}"
    )

    db = SessionLocal()

    try:
        persistence = RecipePersistence(db)

        recipe = persistence.save(normalized_data)

        print(
            f"Recipe saved: "
            f"{recipe.id} - {recipe.name}"
        )

        for item in recipe.ingredients:
            print(
                f"- {item.ingredient.name}: "
                f"{item.quantity} "
                f"{item.unit}"
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()