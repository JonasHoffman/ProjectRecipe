from app.normalizer.recipe import RecipeNormalizer


normalizer = RecipeNormalizer()


def test_ingredients():
    cases = [
        {
            "input": "1/2 xícara (chá) de óleo",
            "group": "Massa",
            "expected": {
                "name": "óleo",
                "quantity": "1/2",
                "unit": "xícara (chá)",
                "details": None,
                "group": "Massa",
                "optional": False,
            },
        },
        {
            "input": "3 cenouras médias raladas",
            "group": "Massa",
            "expected": {
                "name": "cenouras",
                "quantity": "3",
                "unit": None,
                "details": "médias raladas",
                "group": "Massa",
                "optional": False,
            },
        },
        {
            "input": "2 e 1/2 xícaras (chá) de farinha de trigo",
            "group": "Massa",
            "expected": {
                "name": "farinha de trigo",
                "quantity": "2 e 1/2",
                "unit": "xícaras (chá)",
                "details": None,
                "group": "Massa",
                "optional": False,
            },
        },
        {
            "input": "4 ovos",
            "group": "Massa",
            "expected": {
                "name": "ovos",
                "quantity": "4",
                "unit": None,
                "details": None,
                "group": "Massa",
                "optional": False,
            },
        },
        {
            "input": "1 caixinha ou lata de leite condensado",
            "group": "Ingredientes da cobertura",
            "expected": {
                "name": "leite condensado",
                "quantity": "1",
                "unit": "caixinha ou lata",
                "details": None,
                "group": "Ingredientes da cobertura",
                "optional": False,
            },
        },
        {
            "input": "200 gramas de granulado (opcional)",
            "group": "Ingredientes da cobertura",
            "expected": {
                "name": "granulado",
                "quantity": "200",
                "unit": "gramas",
                "details": None,
                "group": "Ingredientes da cobertura",
                "optional": True,
            },
        },
        {
            "input": "sal a gosto",
            "group": "Tempero",
            "expected": {
                "name": "sal",
                "quantity": None,
                "unit": None,
                "details": "a gosto",
                "group": "Tempero",
                "optional": False,
            },
        },
        {
            "input": "1 colher (sopa) colorau",
            "group": None,
            "expected": {
                "name": "colorau",
                "quantity": "1",
                "unit": "colher (sopa)",
                "details": None,
                "group": None,
                "optional": False,
            },
        },
        {
            "input": "1 ou 2 laranjas",
            "group": None,
            "expected": {
                "name": "laranjas",
                "quantity": "1 ou 2",
                "unit": None,
                "details": None,
                "group": None,
                "optional": False,
            },
        },
        {
            "input": "40 ml de de pinga",
            "group": None,
            "expected": {
                "name": "pinga",
                "quantity": "40",
                "unit": "ml",
                "details": None,
                "group": None,
                "optional": False,
            },
        },
        {
            "input": "3 peitos de frango cortados em cubos",
            "group": None,
            "expected": {
                "name": "frango",
                "quantity": "3",
                "unit": "peitos",
                "details": "cortados em cubos",
                "group": None,
                "optional": False,
            },
        },
        {
            "input": "1 colher (sopa) de amido de milho, dissolvido em 50 ml de água",
            "group": None,
            "expected": {
                "name": "amido de milho",
                "quantity": "1",
                "unit": "colher (sopa)",
                "details": "dissolvido em 50 ml de água",
                "group": None,
                "optional": False,
            },
        },
        {
            "input": "1 dente de alho (pequeno) bem espremido",
            "group": None,
            "expected": {
                "name": "alho",
                "quantity": "1",
                "unit": "dente",
                "details": "(pequeno) bem espremido",
                "group": None,
                "optional": False,
            },
        },
        {
            "input": "4 batatas grande descascada em rodelas de 0,5 centímetro de espessura",
            "group": None,
            "expected": {
                "name": "batatas",
                "quantity": "4",
                "unit": None,
                "details": "grande descascada em rodelas de 0,5 centímetro de espessura",
                "group": None,
                "optional": False,
            },
        },
        
    ]

    for case in cases:
        result = normalizer.normalize_ingredient(
            case["input"],
            case["group"],
        )

        assert result == case["expected"], (
            f"\nIngrediente: {case['input']}"
            f"\nEsperado: {case['expected']}"
            f"\nObtido: {result}"
        )


if __name__ == "__main__":
    test_ingredients()
    print("Todos os testes passaram!")