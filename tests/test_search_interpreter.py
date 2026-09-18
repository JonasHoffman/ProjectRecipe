from app.search.interpreter import RecipeSearchInterpreter


def main():
    interpreter = RecipeSearchInterpreter()

    test_cases = [
        "quero uma receita com frango",
        "quero uma receita com frango e batata",
        "quero uma receita com chocolate que fique pronta em até 30 minutos",
        "preciso de uma receita com frango e arroz em até 40 minutos",
    ]

    for text in test_cases:
        result = interpreter.interpret(text)

        print()
        print("Input:", text)
        print("Ingredients:", result.ingredients)
        print(
            "Max preparation time:",
            result.max_preparation_time,
        )


if __name__ == "__main__":
    main()