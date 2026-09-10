
from app.scraper.http_client import fetch_page
from app.scraper.tudogostoso.parser import TudoGostosoParser


url = "https://www.tudogostoso.com.br/receita/1020-bolo-de-cenoura.html"

html = fetch_page(url)

parser = TudoGostosoParser()

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


print("\nUtensils:")

for utensil in recipe["utensils"]:
    print(f"- {utensil}")


print(
    "\nPreparation time:",
    recipe["preparation_time"]
)


print(
    "Servings:",
    f"{recipe['servings']} porções"
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

