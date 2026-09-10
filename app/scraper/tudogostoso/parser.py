import re

from bs4 import BeautifulSoup

from app.scraper.base import RecipeParser


class TudoGostosoParser(RecipeParser):

    def parse(self, html):

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        title = soup.find(
            "span",
            class_="u-title-page"
        )

        preparation_time = soup.select_one(
            ".recipe-steps-info-item time"
        )

        servings_element = soup.select_one(
            ".recipe-section.recipe-ingredients h2"
        )

        image = soup.find(
            "img",
            alt=title.text.strip()
        )

        servings = None

        if servings_element:

            servings_text = servings_element.get_text(
                " ",
                strip=True
            )

            match = re.search(
                r"\((\d+)\s*porções?\)",
                servings_text
            )

            if match:

                servings = int(
                    match.group(1)
                )

        ingredients = self.parse_ingredients(
            soup
        )

        steps = self.parse_steps(
            soup
        )

        utensils = self.parse_utensils(
            soup
        )

        rating = self.parse_rating(
            soup
        )

        rating_count = self.parse_rating_count(
            soup
        )

        return {

            "title": title.text.strip(),

            "ingredients": ingredients,

            "steps": steps,

            "preparation_time": (
                preparation_time.text.strip()
                if preparation_time
                else None
            ),

            "servings": servings,

            "image_url": (
                image["src"]
                if image
                else None
            ),

            "utensils": utensils,

            "rating": rating,

            "rating_count": rating_count,

        }

    def parse_ingredients(self, soup):

        ingredients_section = soup.select_one(
            ".recipe-section.recipe-ingredients"
        )

        if not ingredients_section:

            return []

        groups = []

        current_group = None

        for element in ingredients_section.find_all(
            ["h3", "span"],
            class_=[
                "recipe-ingredients-subtitle",
                "recipe-ingredients-item-label",
            ]
        ):

            if (
                element.name == "h3"
                and "recipe-ingredients-subtitle"
                in element.get("class", [])
            ):

                current_group = {

                    "group": element.get_text(
                        " ",
                        strip=True
                    ).rstrip(":"),

                    "items": [],

                }

                groups.append(
                    current_group
                )

            elif (
                element.name == "span"
                and "recipe-ingredients-item-label"
                in element.get("class", [])
            ):

                ingredient = element.get_text(
                    " ",
                    strip=True
                )

                if current_group:

                    current_group["items"].append(
                        ingredient
                    )

                else:

                    groups.append(
                        {
                            "group": None,
                            "items": [ingredient],
                        }
                    )

        return groups

    def parse_steps(self, soup):

        steps_section = soup.select_one(
            ".recipe-section.recipe-steps"
        )

        if not steps_section:

            return []

        groups = []

        current_group = None

        for element in steps_section.find_all(
            ["h3", "div"],
            class_=[
                "recipe-steps-title",
                "recipe-steps-text",
            ]
        ):

            if (
                element.name == "h3"
                and "recipe-steps-title"
                in element.get("class", [])
            ):

                current_group = {

                    "group": element.get_text(
                        " ",
                        strip=True
                    ).rstrip(":"),

                    "items": [],

                }

                groups.append(
                    current_group
                )

            elif (
                element.name == "div"
                and "recipe-steps-text"
                in element.get("class", [])
            ):

                step = element.get_text(
                    " ",
                    strip=True
                )

                if current_group:

                    current_group["items"].append(
                        step
                    )

                else:

                    groups.append(
                        {
                            "group": None,
                            "items": [step],
                        }
                    )

        return groups

    def parse_utensils(self, soup):

        utensils = []

        for element in soup.select(
            ".recipe-equipments-item-label"
        ):

            utensil = element.get_text(
                " ",
                strip=True
            )

            if utensil:

                utensils.append(
                    utensil
                )

        return utensils

    def parse_rating(self, soup):

        rating = soup.select_one(
            ".rating-grade .u-bold"
        )

        if not rating:

            return None

        try:

            return float(
                rating.get_text(
                    " ",
                    strip=True
                ).replace(",", ".")
            )

        except ValueError:

            return None

    def parse_rating_count(self, soup):

        votes = soup.select_one(
            ".rating-votes"
        )

        if not votes:

            return None

        text = votes.get_text(
            " ",
            strip=True
        )

        match = re.search(
            r"\(([\d.]+)\s+avaliações?\)",
            text
        )

        if not match:

            return None

        return int(
            match.group(1).replace(".", "")
        )