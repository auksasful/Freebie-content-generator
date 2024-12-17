

from typing_extensions import TypedDict


class Recipe(TypedDict):
  name: str
  ingredients: list[str]
  cooking_time: str
  instructions: list[str]
  cooking_tips: str
  health_benefits: str
  nutritional_information: str



class RecipeName(TypedDict):
  name: str

class RecipesNames(TypedDict):
  recipes: list[RecipeName]