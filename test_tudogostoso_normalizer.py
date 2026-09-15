from app.scraper.http_client import fetch_page
from app.scraper.tudogostoso.parser import TudoGostosoParser
from app.normalizer.recipe import RecipeNormalizer


url = "https://www.tudogostoso.com.br/receita/23-bolo-de-cenoura.html"

html = fetch_page(url)

parser = TudoGostosoParser()
recipe = parser.parse(html)

normalizer = RecipeNormalizer()

normalized_recipe = normalizer.normalize(
    recipe,
    source_name="TudoGostoso",
    source_url=url,
)


def test_recipe():

    assert normalized_recipe["name"] == "Bolo de cenoura"

    assert normalized_recipe["preparation_time"] == 40

    assert normalized_recipe["servings"] == 8

    assert normalized_recipe["source_name"] == "TudoGostoso"

    assert normalized_recipe["source_url"] == url

    assert normalized_recipe["image_url"] is not None

    assert len(normalized_recipe["ingredients"]) == 10

    assert normalized_recipe["ingredients"][0] == {
        "name": "óleo",
        "quantity": "1/2",
        "unit": "xícara (chá)",
        "details": None,
        "group": "Massa",
        "optional": False,
    }

    assert normalized_recipe["ingredients"][1] == {
        "name": "cenouras",
        "quantity": "3",
        "unit": None,
        "details": "médias raladas",
        "group": "Massa",
        "optional": False,
    }

    assert normalized_recipe["ingredients"][2] == {
        "name": "ovos",
        "quantity": "4",
        "unit": None,
        "details": None,
        "group": "Massa",
        "optional": False,
    }


if __name__ == "__main__":
    test_recipe()

    print("TudoGostoso normalization test passed!")