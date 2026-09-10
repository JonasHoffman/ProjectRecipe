
from bs4 import BeautifulSoup

from app.scraper.base import RecipeParser


class PanelinhaParser(RecipeParser):

    def parse(self, html):
        soup = BeautifulSoup(html, "html.parser")

        return {
            "title": self.parse_title(soup),
            "ingredients": self.parse_ingredients(soup),
            "steps": self.parse_steps(soup),
            "preparation_time": self.parse_preparation_time(soup),
            "servings": self.parse_servings(soup),
            "image_url": self.parse_image(soup),
        }

    def parse_title(self, soup):
        title = soup.select_one(
            "h1.headerRecipeImageH1"
        )

        if not title:
            return None

        return title.get_text(
            " ",
            strip=True
        )

    
    
    def parse_ingredients(self, soup):
        ingredient_groups = soup.select(".psB1-oM")

        if not ingredient_groups:
            return []

        groups = []

        for group in ingredient_groups:
            title = group.select_one(
                ".tDivT"
            )

            ingredients_list = group.select_one(
                ".blockIngredientListingsctn ul"
            )

            if not ingredients_list:
                continue

            ingredients = []

            for item in ingredients_list.find_all("li"):
                ingredient = item.get_text(
                    " ",
                    strip=True
                )

                if ingredient:
                    ingredients.append(ingredient)

            if not ingredients:
                continue

            groups.append(
                {
                    "group": (
                        title.get_text(
                            " ",
                            strip=True
                        )
                        if title
                        else None
                    ),
                    "items": ingredients,
                }
            )

        return groups





    def parse_steps(self, soup):
        steps = []
        current_group = None

        elements = soup.select(
            ".tDivT, li[id^='recipe_bk_'][id$='_fs']"
        )

        for element in elements:

            if element.name == "h3":
                current_group = {
                    "group": element.get_text(
                        " ",
                        strip=True
                    ),
                    "items": [],
                }

                steps.append(current_group)

            elif element.name == "li":
                step = element.get_text(
                    " ",
                    strip=True
                )

                if not step:
                    continue

                if current_group:
                    current_group["items"].append(step)

                else:
                    steps.append(
                        {
                            "group": None,
                            "items": [step],
                        }
                    )

        return steps

    def parse_preparation_time(self, soup):
        stats = soup.select_one(".stats")

        if not stats:
            return None

        for item in stats.find_all("div"):
            label = item.find("dt")
            value = item.find("dd")

            if not label or not value:
                continue

            if label.get_text(
                " ",
                strip=True
            ).lower() == "tempo de preparo":
                return value.get_text(
                    " ",
                    strip=True
                )

        return None

    def parse_servings(self, soup):
        stats = soup.select_one(".stats")

        if not stats:
            return None

        for item in stats.find_all("div"):
            label = item.find("dt")
            value = item.find("dd")

            if not label or not value:
                continue

            if label.get_text(
                " ",
                strip=True
            ).lower() == "serve":
                return value.get_text(
                    " ",
                    strip=True
                )

        return None

    def parse_image(self, soup):
        image = soup.select_one(
            "img.imgRe"
        )

        if not image:
            return None

        return image.get("src")
