from app.normalizer.recipe import RecipeNormalizer


normalizer = RecipeNormalizer()


data = {
    "title": "  Frango   assado com   batatas ",
    "preparation_time": "1 hora e 30 minutos",
    "servings": "4 porções",
    "steps": [
        {
            "group": None,
            "items": [
                "Tempere o frango.",
                "Coloque em uma assadeira.",
            ],
        },
        {
            "group": "Finalização",
            "items": [
                "Leve ao forno por 30 minutos.",
            ],
        },
    ],
    "ingredients": [
        {
            "group": None,
            "items": [
                "1 kg de frango",
                "2 xícaras de farinha de trigo",
                "3 ovos",
            ],
        },
        {
            "group": "Tempero",
            "items": [
                "2 dentes de alho",
                "sal a gosto",
            ],
        },
    ],
    "image_url": "https://exemplo.com/frango.jpg",
}


result = normalizer.normalize(
    data=data,
    source_name="Teste",
    source_url="https://exemplo.com/receita",
)


print(result)