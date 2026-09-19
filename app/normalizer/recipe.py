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

        value = " ".join(value.split())

        # ---------------------------------------------------------
        # Quantity ranges
        #
        # Examples:
        # 1 ou 2 laranjas
        # 2 ou 3 tomates
        # ---------------------------------------------------------

        range_match = re.match(
            r"^(\d+(?:[.,]\d+)?\s+ou\s+\d+(?:[.,]\d+)?)\s+(.+)$",
            value,
            re.IGNORECASE,
        )

        if range_match:
            return {
                "name": range_match.group(2).strip(),
                "quantity": range_match.group(1).strip(),
                "unit": None,
                "details": parenthetical_details,
                "group": group,
                "optional": optional,
            }

        # ---------------------------------------------------------
        # Quantity + unit
        #
        # Examples:
        # 1 colher (sopa) colorau
        # 1 colher (sopa) de amido de milho
        # 1 xícara (chá) de óleo
        # 200 gramas de granulado
        # 40 ml de pinga
        # ---------------------------------------------------------

        match = re.match(
            r"^("
            r"\d+\s+e\s+\d+/\d+"
            r"|"
            r"\d+/\d+"
            r"|"
            r"\d+(?:[.,]\d+)?"
            r")"
            r"\s+"
            r"("
            r"caixinhas\s+ou\s+latas?"
            r"|"
            r"caixinha\s+ou\s+lata"
            r"|"
            r"xícaras"
            r"|"
            r"xícara"
            r"|"
            r"colheres"
            r"|"
            r"colher"
            r"|"
            r"copos"
            r"|"
            r"copo"
            r"|"
            r"latas"
            r"|"
            r"lata"
            r"|"
            r"dentes"
            r"|"
            r"dente"
            r"|"
            r"peitos"
            r"|"
            r"peito"
            r"|"
            r"quilogramas"
            r"|"
            r"quilograma"
            r"|"
            r"gramas"
            r"|"
            r"grama"
            r"|"
            r"litros"
            r"|"
            r"litro"
            r"|"
            r"kg"
            r"|"
            r"mg"
            r"|"
            r"ml"
            r"|"
            r"g"
            r"|"
            r"l"
            r")"
            r"(?![A-Za-zÀ-ÿ])"
            r"\s*(\([^)]*\))?"
            r"\s*(?:de\s+)?"
            r"(.+)$",
            value,
            re.IGNORECASE,
        )

        if match:
            quantity = match.group(1)
            unit = match.group(2)
            unit_detail = match.group(3)
            remainder = match.group(4).strip()

            if unit_detail:
                unit = f"{unit} {unit_detail}"

            # Remove duplicated "de".
            #
            # Example:
            # 40 ml de de pinga
            # -> pinga
            remainder = re.sub(
                r"^(?:de\s+)+",
                "",
                remainder,
                flags=re.IGNORECASE,
            )

            # ---------------------------------------------------------
            # Extract parenthetical details from the middle.
            #
            # Example:
            # 1 dente de alho (pequeno) bem espremido
            #
            # remainder before:
            # alho (pequeno) bem espremido
            #
            # remainder after:
            # alho bem espremido
            #
            # parenthetical_details:
            # (pequeno)
            # ---------------------------------------------------------

            inline_parenthetical = re.search(
                r"(\([^)]*\))",
                remainder,
            )

            if inline_parenthetical:
                parenthetical_text = inline_parenthetical.group(1)

                remainder = (
                    remainder[:inline_parenthetical.start()]
                    + remainder[inline_parenthetical.end():]
                ).strip()

                remainder = " ".join(remainder.split())

                if parenthetical_details:
                    parenthetical_details = (
                        f"{parenthetical_text} "
                        f"{parenthetical_details}"
                    )
                else:
                    parenthetical_details = parenthetical_text

            ingredient_details = None

            ingredient_details = None

            # -----------------------------------------------------
            # Separate ingredient from preparation details.
            #
            # Example:
            # 1 colher (sopa) de amido de milho,
            # dissolvido em 50 ml de água
            # -----------------------------------------------------

            comma_match = re.match(
                r"^(.+?),\s*(.+)$",
                remainder,
            )

            if comma_match:
                remainder = comma_match.group(1).strip()
                ingredient_details = comma_match.group(2).strip()

            # -----------------------------------------------------
            # Preparation details without comma.
            #
            # Examples:
            # 1 colher de farinha peneirada
            # 1 colher de açúcar misturado
            # -----------------------------------------------------

            if ingredient_details is None:
                detail_match = re.match(
                    r"^(.+?)\s+("
                    r"cortados?\s+em\s+.+|"
                    r"cortadas?\s+em\s+.+|"
                    r"picados?\s+em\s+.+|"
                    r"picadas?\s+em\s+.+|"
                    r"descascados?\s+em\s+.+|"
                    r"descascadas?\s+em\s+.+|"
                    r"ralados?\s+em\s+.+|"
                    r"raladas?\s+em\s+.+|"
                    r"fatiados?\s+em\s+.+|"
                    r"fatiadas?\s+em\s+.+|"
                    r"cortados?|"
                    r"cortadas?|"
                    r"picados?|"
                    r"picadas?|"
                    r"descascados?|"
                    r"descascadas?|"
                    r"ralados?|"
                    r"raladas?|"
                    r"fatiados?|"
                    r"fatiadas?|"
                    r"amassados?|"
                    r"amassadas?|"
                    r"cozidos?|"
                    r"cozidas?|"
                    r"derretidos?|"
                    r"derretidas?"
                    r")$",
                    remainder,
                    re.IGNORECASE,
                )

                if detail_match:
                    remainder = detail_match.group(1).strip()
                    ingredient_details = detail_match.group(2).strip()

            details = (
                ingredient_details
                or parenthetical_details
            )

            return {
                "name": remainder,
                "quantity": quantity.strip(),
                "unit": unit.strip(),
                "details": details,
                "group": group,
                "optional": optional,
            }

        # ---------------------------------------------------------
        # Quantity + ingredient with unit
        #
        # Examples:
        # 3 peitos de frango cortados em cubos
        # 2 dentes de alho picados
        # 1 dente de alho (pequeno) bem espremido
        # ---------------------------------------------------------

        match = re.match(
            r"^("
            r"\d+\s+e\s+\d+/\d+"
            r"|"
            r"\d+/\d+"
            r"|"
            r"\d+(?:[.,]\d+)?"
            r")"
            r"\s+"
            r"(xícaras|xícara|"
            r"colheres|colher|"
            r"copos|copo|"
            r"peitos|peito|"
            r"dentes|dente|"
            r"latas|lata|"
            r"quilogramas|quilograma|"
            r"gramas|grama|"
            r"litros|litro|"
            r"kg|mg|ml|g|l)"
            r"(?![A-Za-zÀ-ÿ])"
            r"\s+"
            r"(?:de\s+)?"
            r"(.+)$",
            value,
            re.IGNORECASE,
        )

        if match:
            quantity = match.group(1)
            unit = match.group(2)
            remainder = match.group(3).strip()

            ingredient_name = remainder
            details = parenthetical_details

            # -----------------------------------------------------
            # Extract parenthetical details from the middle.
            #
            # Example:
            # 1 dente de alho (pequeno) bem espremido
            #
            # -> alho
            # -> (pequeno) bem espremido
            # -----------------------------------------------------

            inline_parenthetical = re.search(
                r"(\([^)]*\))",
                remainder,
            )

            if inline_parenthetical:
                parenthetical_text = inline_parenthetical.group(1)

                remainder = (
                    remainder[:inline_parenthetical.start()]
                    + remainder[inline_parenthetical.end():]
                ).strip()

                remainder = " ".join(remainder.split())

                if parenthetical_details:
                    parenthetical_details = (
                        f"{parenthetical_text} "
                        f"{parenthetical_details}"
                    )
                else:
                    parenthetical_details = parenthetical_text

                details = parenthetical_details

            # -----------------------------------------------------
            # Separate preparation details.
            #
            # Examples:
            # frango cortados em cubos
            # alho picado
            # batatas descascadas
            # -----------------------------------------------------

            detail_match = re.match(
                r"^(.+?)\s+("
                r"cortados?\s+em\s+.+|"
                r"cortadas?\s+em\s+.+|"
                r"picados?\s+em\s+.+|"
                r"picadas?\s+em\s+.+|"
                r"descascados?\s+em\s+.+|"
                r"descascadas?\s+em\s+.+|"
                r"ralados?\s+em\s+.+|"
                r"raladas?\s+em\s+.+|"
                r"fatiados?\s+em\s+.+|"
                r"fatiadas?\s+em\s+.+|"
                r"cortados?|"
                r"cortadas?|"
                r"picados?|"
                r"picadas?|"
                r"descascados?|"
                r"descascadas?|"
                r"ralados?|"
                r"raladas?|"
                r"fatiados?|"
                r"fatiadas?|"
                r"amassados?|"
                r"amassadas?|"
                r"cozidos?|"
                r"cozidas?|"
                r"derretidos?|"
                r"derretidas?"
                r")$",
                remainder,
                re.IGNORECASE,
            )

            if detail_match:
                ingredient_name = detail_match.group(1).strip()

                preparation_details = (
                    detail_match.group(2).strip()
                )

                if details:
                    details = (
                        f"{details} "
                        f"{preparation_details}"
                    )
                else:
                    details = preparation_details

            return {
                "name": ingredient_name,
                "quantity": quantity.strip(),
                "unit": unit.strip(),
                "details": details,
                "group": group,
                "optional": optional,
            }

        # ---------------------------------------------------------
        # Quantity + ingredient
        #
        # Examples:
        # 4 ovos
        # 3 cenouras médias raladas
        # 4 batatas grandes descascadas
        # ---------------------------------------------------------

        match = re.match(
            r"^("
            r"\d+\s+e\s+\d+/\d+"
            r"|"
            r"\d+/\d+"
            r"|"
            r"\d+(?:[.,]\d+)?"
            r")"
            r"\s+"
            r"(.+)$",
            value,
            re.IGNORECASE,
        )

        if match:
            quantity = match.group(1)
            remainder = match.group(2).strip()

            words = remainder.split()

            name = words[0]

            details = (
                " ".join(words[1:])
                or parenthetical_details
            )

            return {
                "name": name.strip(),
                "quantity": quantity.strip(),
                "unit": None,
                "details": details,
                "group": group,
                "optional": optional,
            }

        # ---------------------------------------------------------
        # Ingredient + "a gosto"
        #
        # Example:
        # sal a gosto
        # ---------------------------------------------------------

        match = re.match(
            r"^(.+?)\s+(a gosto)$",
            value,
            re.IGNORECASE,
        )

        if match:
            return {
                "name": match.group(1).strip(),
                "quantity": None,
                "unit": None,
                "details": match.group(2).strip(),
                "group": group,
                "optional": optional,
            }

        # ---------------------------------------------------------
        # Fallback
        # ---------------------------------------------------------

        return {
            "name": value,
            "quantity": None,
            "unit": None,
            "details": parenthetical_details,
            "group": group,
            "optional": optional,
        }