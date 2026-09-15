
from app.scraper.http_client import fetch_page
from app.scraper.receitaria.parser import ReceiteriaParser
from app.normalizer.recipe import RecipeNormalizer


url = "https://www.receiteria.com.br/receita/bolo-de-chocolate-rapido-e-molhadinho/"

html = fetch_page(url)

parser = ReceiteriaParser()
recipe = parser.parse(html)

normalizer = RecipeNormalizer()

normalized_recipe = normalizer.normalize(
    recipe,
    source_name="Receiteria",
    source_url=url,
)


def test_recipe():

    assert normalized_recipe["name"] == (
        "Bolo de chocolate fácil e molhadinho"
    )

    assert normalized_recipe["preparation_time"] == 60

    assert normalized_recipe["servings"] == 9

    assert normalized_recipe["source_name"] == "Receiteria"

    assert normalized_recipe["source_url"] == url

    assert normalized_recipe["image_url"] is not None
    print(normalized_recipe["ingredients"][2])
    assert len(normalized_recipe["ingredients"]) == 10

    assert normalized_recipe["ingredients"][0] == {
        "name": "ovos",
        "quantity": "2",
        "unit": None,
        "details": None,
        "group": "Ingredientes da massa",
        "optional": False,
    }

    assert normalized_recipe["ingredients"][1] == {
        "name": "açúcar",
        "quantity": "1",
        "unit": "xícara de chá",
        "details": None,
        "group": "Ingredientes da massa",
        "optional": False,
    }

    assert normalized_recipe["ingredients"][2] == {
        "name": "chocolate em pó",
        "quantity": "1",
        "unit": "xícara de chá",
        "details": "(ou achocolatado)",
        "group": "Ingredientes da massa",
        "optional": False,
    }

    assert normalized_recipe["ingredients"][9] == {
        "name": "granulado",
        "quantity": "200",
        "unit": "gramas",
        "details": None,
        "group": "Ingredientes da cobertura",
        "optional": True,
    }


if __name__ == "__main__":
    test_recipe()

    print("Receiteria normalization test passed!")

