from app.database.database import SessionLocal
from app.normalizer.recipe import RecipeNormalizer
from app.persistence.recipe import RecipePersistence
from app.scraper.http_client import fetch_page
from app.scraper.tudogostoso.parser import TudoGostosoParser


RECIPES = [
    "https://www.tudogostoso.com.br/receita/23-bolo-de-cenoura.html",
    'https://www.tudogostoso.com.br/receita/166886-lasanha-de-berinjela-e-abobrinha.html',
    'https://www.tudogostoso.com.br/receita/98902-torta-salgada.html',
    'https://www.tudogostoso.com.br/receita/1624-macarrao-a-carbonara.html',
    'https://www.tudogostoso.com.br/receita/31593-pudim-de-leite-condensado.html',
    'https://www.tudogostoso.com.br/receita/4683-bolinho-de-chuva.html',
    'https://www.tudogostoso.com.br/receita/58-tabule.html',
    'https://www.tudogostoso.com.br/receita/2462-strogonoff-de-frango.html',
    'https://www.tudogostoso.com.br/receita/301775-brownie-de-chocolate-na-air-fryer.html',
    'https://www.tudogostoso.com.br/receita/109052-file-de-peixe-assado.html',
    'https://www.tudogostoso.com.br/receita/2998-feijoada.html',
    'https://www.tudogostoso.com.br/receita/2085-yakissoba-da-casa.html',
    "https://www.tudogostoso.com.br/receita/309779-bolo-de-chocolate-simples.html",
    "https://www.tudogostoso.com.br/receita/21560-bolo-de-fuba-simples.html",
    "https://www.tudogostoso.com.br/receita/64879-almondegas.html",
    "https://www.tudogostoso.com.br/receita/53915-estrogonofe-de-carne-simples.html",
    "https://www.tudogostoso.com.br/receita/10254-fricasse-de-frango.html",
    "https://www.tudogostoso.com.br/receita/897-frango-xadrez.html",
    "https://www.tudogostoso.com.br/receita/162495-frango-desfiado-na-panela-de-pressao.html",
    "https://www.tudogostoso.com.br/receita/30068-file-de-frango-empanado.html",
    "https://www.tudogostoso.com.br/receita/112-bobo-de-camarao.html",
    "https://www.tudogostoso.com.br/receita/133817-moqueca-de-peixe-facil.html",
    "https://www.tudogostoso.com.br/receita/44199-molho-branco-simples.html",
    "https://www.tudogostoso.com.br/receita/59-pure-de-batata.html",
    "https://www.tudogostoso.com.br/receita/82681-massa-de-panqueca.html",
    "https://www.tudogostoso.com.br/receita/13110-panqueca-americana.html",
    "https://www.tudogostoso.com.br/receita/13953-bolo-de-laranja.html",

]


def main():
    parser = TudoGostosoParser()
    normalizer = RecipeNormalizer()

    db = SessionLocal()

    try:
        persistence = RecipePersistence(db)

        for url in RECIPES:
            print(f"\nProcessing: {url}")

            html = fetch_page(url)

            raw_recipe = parser.parse(html)
            print("\nRaw ingredient groups:")

            for group in raw_recipe["ingredients"]:
                print("GROUP:", repr(group["group"]))
            print("\nRaw ingredients:")

            for index, ingredient_group in enumerate(
                raw_recipe["ingredients"]
            ):
                print(f"\nGroup {index}:")

                for item in ingredient_group["items"]:
                    print("-", repr(item))
            normalized_recipe = normalizer.normalize(
                raw_recipe,
                "TudoGostoso",
                url,
            )
            print("\nNormalized ingredients:")

            for index, ingredient in enumerate(
                normalized_recipe["ingredients"]
            ):
                print(index, ingredient)

            recipe = persistence.save(
                normalized_recipe
            )

            print(
                f"Saved: {recipe.id} - {recipe.name}"
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()