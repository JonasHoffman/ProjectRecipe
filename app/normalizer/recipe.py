import re


class RecipeNormalizer:

    def normalize(
        self,
        data: dict,
        source_name: str,
        source_url: str,
    ) -> dict:
        return {
            "name": self.normalize_name(data.get("title")),
            "description": data.get("description"),
            "preparation_time": self.normalize_preparation_time(
                data.get("preparation_time")
            ),
            "servings": self.normalize_servings(
                data.get("servings")
            ),
            "instructions": self.normalize_instructions(
                data.get("steps", [])
            ),
            "source_name": source_name,
            "source_url": source_url,
            "image_url": data.get("image_url"),
            "ingredients": self.normalize_ingredients(
                data.get("ingredients", [])
            ),
        }

    def normalize_name(self, title: str | None) -> str | None:
        if not title:
            return None

        return " ".join(title.split())

    def normalize_preparation_time(
        self,
        value: str | int | None,
    ) -> int | None:

        if value is None:
            return None

        if isinstance(value, int):
            return value

        value = value.lower().strip()

        hours = 0
        minutes = 0

        hour_match = re.search(
            r"(\d+)\s*h(?:ora|oras)?",
            value,
        )

        if hour_match:
            hours = int(hour_match.group(1))

        minute_match = re.search(
            r"(\d+)\s*(?:m|min|mins|minute|minutos?)",
            value,
        )

        if minute_match:
            minutes = int(minute_match.group(1))

        if hours or minutes:
            return hours * 60 + minutes

        number_match = re.search(r"\d+", value)

        if number_match:
            return int(number_match.group())

        return None

    def normalize_servings(
        self,
        value: str | int | None,
    ) -> int | None:

        if value is None:
            return None

        if isinstance(value, int):
            return value

        match = re.search(r"\d+", value)

        if match:
            return int(match.group())

        return None

    def normalize_instructions(
        self,
        groups: list[dict],
    ) -> str:

        instructions = []

        for group in groups:
            group_name = group.get("group")
            items = group.get("items", [])

            if group_name:
                instructions.append(f"{group_name}:")

            instructions.extend(items)
            instructions.append("")

        return "\n".join(instructions).strip()

    def normalize_ingredients(
        self,
        groups: list[dict],
    ) -> list[dict]:

        ingredients = []

        for group in groups:
            group_name = group.get("group")
            items = group.get("items", [])

            for item in items:
                ingredient = self.normalize_ingredient(
                    item,
                    group_name,
                )

                ingredients.append(ingredient)

        return ingredients


    def normalize_ingredient(
        self,
        value: str,
        group: str | None,
    ) -> dict:

        value = value.strip()

        optional = bool(
            re.search(
                r"\(\s*opcional\s*\)",
                value,
                re.IGNORECASE,
            )
        )

        value = re.sub(
            r"\s*\(\s*opcional\s*\)",
            "",
            value,
            flags=re.IGNORECASE,
        ).strip()

        parenthetical_details = None

        parenthetical_match = re.search(
            r"(\([^)]*\))$",
            value,
        )

        if parenthetical_match:
            parenthetical_details = parenthetical_match.group(1)
            value = value[:parenthetical_match.start()].strip()

        # Pattern:
        # quantity + compound unit + "de" + ingredient
        #
        # Example:
        # 1 xícara de chá de açúcar
        #
        # Result:
        # quantity = 1
        # unit = xícara de chá
        # name = açúcar
        match = re.match(
            r"^(\d+(?:\s+e\s+\d+/\d+)?|\d+/\d+|\d+(?:[.,]\d+)?)\s+(.+?\s+de\s+\w+)\s+de\s+(.+)$",
            value,
            re.IGNORECASE,
        )

        if match:
            quantity = match.group(1)
            unit = match.group(2)
            name = match.group(3)

            return {
                "name": name.strip(),
                "quantity": quantity.strip(),
                "unit": unit.strip(),
                "details": None,
                "group": group,
                "optional": optional,
                "details": parenthetical_details,
            }

        # Pattern:
        # quantity + unit + "de" + ingredient
        #
        # Examples:
        # 1/2 xícara (chá) de óleo
        # 2 xícaras de farinha de trigo
        # 1 colher (sopa) de fermento
        match = re.match(
            r"^(\d+(?:\s+e\s+\d+/\d+)?|\d+/\d+|\d+(?:[.,]\d+)?)\s+(.+?)\s+de\s+(.+)$",
            value,
            re.IGNORECASE,
        )

        if match:
            quantity = match.group(1)
            unit = match.group(2)
            name = match.group(3)

            return {
                "name": name.strip(),
                "quantity": quantity.strip(),
                "unit": unit.strip(),
                "details": None,
                "group": group,
                "optional": optional,
                "details": parenthetical_details,
            }

        # Pattern:
        # quantity + ingredient + details
        #
        # Example:
        # 3 cenouras médias raladas
        #
        # Result:
        # name = cenouras
        # quantity = 3
        # details = médias raladas
        match = re.match(
            r"^(\d+(?:[.,]\d+)?)\s+(\S+)(?:\s+(.+))?$",
            value,
            re.IGNORECASE,
        )

        if match:
            quantity = match.group(1)
            name = match.group(2)
            details = match.group(3)

            return {
                "name": name.strip(),
                "quantity": quantity.strip(),
                "unit": None,
                "details": details.strip() if details else None,
                "group": group,
                "optional": optional,
                "details": parenthetical_details,
            }

        # Pattern:
        # ingredient + "a gosto"
        #
        # Example:
        # sal a gosto
        match = re.match(
            r"^(.+?)\s+(a gosto)$",
            value,
            re.IGNORECASE,
        )

        if match:
            name = match.group(1)
            details = match.group(2)

