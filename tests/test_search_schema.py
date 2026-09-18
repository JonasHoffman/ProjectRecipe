from app.schemas.recipe import RecipeSearchQuery


def main():
    search = RecipeSearchQuery(
        ingredients=["chicken", "potato"],
        max_preparation_time=40,
    )

    print("Ingredients:", search.ingredients)
    print("Max preparation time:", search.max_preparation_time)

    assert search.ingredients == ["chicken", "potato"]
    assert search.max_preparation_time == 40

    print("Search schema test passed!")


if __name__ == "__main__":
    main()