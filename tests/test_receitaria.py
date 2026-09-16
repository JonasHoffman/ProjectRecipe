
from app.scraper.http_client import fetch_page
from app.scraper.receitaria.parser import ReceiteriaParser


url = "https://www.receiteria.com.br/receita/bolo-de-chocolate-rapido-e-molhadinho/"

html = fetch_page(url)

parser = ReceiteriaParser()

recipe = parser.parse(html)


print("Title:", recipe["title"])


print("\nIngredients:")

for group in recipe["ingredients"]:

    if group["group"]:
        print(f"\n{group['group']}:")

    for ingredient in group["items"]:
        print(f"- {ingredient}")


print("\nPreparation steps:")

for group in recipe["steps"]:

    if group["group"]:
        print(f"\n{group['group']}:")

    for step in group["items"]:
        print(f"- {step}")


print(
    "\nPreparation time:",
    recipe["preparation_time"]
)


print(
    "Servings:",
    recipe["servings"]
)


print(
    "Rating:",
    recipe["rating"]
)


print(
    "Rating count:",
    recipe["rating_count"]
)


print(
    "Image URL:",
    recipe["image_url"]
)

