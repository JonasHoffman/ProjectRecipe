
from abc import ABC, abstractmethod


class RecipeParser(ABC):

    @abstractmethod
    def parse(self, html):
        pass

