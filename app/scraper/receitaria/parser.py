
import re

from bs4 import BeautifulSoup

from app.scraper.base import RecipeParser


class ReceiteriaParser(RecipeParser):

    def parse(self, html):

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        title = soup.select_one(
            "div.title h1"
        )

        image = soup.select_one(
            ".foto-capa img"
        )

        servings = soup.select_one(
            ".infos-novo .bread span"
        )

        preparation_time = soup.select_one(
            ".infos-novo time"
        )

        ingredients = self.parse_ingredients(
            soup
        )

        steps = self.parse_steps(
            soup
        )

        rating = self.parse_rating(
            soup
        )

        rating_count = self.parse_rating_count(
            soup
        )

        return {

            "title": (
                title.get_text(
                    " ",
                    strip=True
                )
                if title
                else None
            ),

            "ingredients": ingredients,

            "steps": steps,

            "preparation_time": (
                preparation_time.get_text(
                    " ",
                    strip=True
                )
                if preparation_time
                else None
            ),

            "servings": (
                servings.get_text(
                    " ",
                    strip=True
                )
                if servings
                else None
            ),

            "image_url": (
                image.get("src")
                if image
                else None
            ),

            "rating": rating,

            "rating_count": rating_count,

        }

    def parse_ingredients(self, soup):

        ingredients_section = soup.select_one(
            "#rc-ingredientes"
        )

        if not ingredients_section:

            return []

        groups = []

        for heading in ingredients_section.select(
            "h2"
        ):

            group = {

                "group": heading.get_text(
                    " ",
                    strip=True
                ),

                "items": [],

            }

            ul = heading.find_next(
                "ul"
            )

            if not ul:

                continue

            for label in ul.select(
                "label"
            ):

                ingredient = label.get_text(
                    " ",
                    strip=True
                )

                if ingredient:

                    group["items"].append(
                        ingredient
                    )

            if group["items"]:

                groups.append(
                    group
                )

        return groups

    def parse_steps(self, soup):

        steps_section = soup.select_one(
            "ol.lista-preparo-1"
        )

        if not steps_section:

            return []

        steps = []

        for step in steps_section.select(
            "li span"
        ):

            text = step.get_text(
                " ",
                strip=True
            )

            if text:

                steps.append(
                    text
                )

        return [

            {

                "group": None,

                "items": steps,

            }

        ]

    def parse_rating(self, soup):

        rating = soup.select_one(
            ".rating-number"
        )

        if not rating:

            return None

        text = rating.get_text(
            " ",
            strip=True
        )

        match = re.search(
            r"([\d]+[,.]?\d*)\s+de\s+5",
            text
        )

        if not match:

            return None

        return float(
            match.group(1).replace(
                ",",
                "."
            )
        )

    def parse_rating_count(self, soup):

        rating = soup.select_one(
            ".rating-number"
        )

        if not rating:

            return None

        text = rating.get_text(
            " ",
            strip=True
        )

        match = re.search(
            r"\(([\d.]+)\)",
            text
        )

        if not match:

            return None

        return int(
            match.group(1).replace(
                ".",
                ""
            )
        )

