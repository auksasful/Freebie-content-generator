
from dataclasses import dataclass


@dataclass
class RecipeBookSettings:
    width = 1200
    height = 800
    website_url = 'https://www.google.com'

    titles_prompt_1 = "Generate a list of 20 very general recipe titles for "
    titles_prompt_2 = ". Each should be unique, don't repeat yourself."
    generation_prompt_1 = "Generate one healthy recipe for "
    generation_prompt_2 = " that is good for quick fat loss. Include at least 2 ingredients, but no more than 5 ingredients. Provide cooking time. Provide cooking tips. Provide nutritional information. Make the instructions short but understandable. Do not use fractions of numbers."
    system_prompt = ""
    cover_page_image1_prompt = "Photo realistic image. Far view of "
    cover_page_image2_prompt = "Photo realistic image. Close up view of "
    image_prompt_default = "Photo realistic image of a dish "
    image_prompt_bottom_1 = "Entire image of "
    image_prompt_bottom_2 = " related things close view"

@dataclass
class TipsBookSettings:
    width = 1200
    height = 800
    website_url = 'https://www.google.com'

    titles_prompt_1 = "Generate a list of 20 very general up to 8 words tip titles for "
    titles_prompt_2 = ". Each should be unique, don't repeat yourself. Do not use more than 8 words."
    generation_prompt_1 = "Generate one tip for "
    generation_prompt_2 = " that is useful. Include at least 2 instruction steps, but no more than 5 instruction steps. Provide description. Make the instructions short but understandable. Do not use fractions of numbers."
    system_prompt = ""
    cover_page_image1_prompt = "Photo realistic image. Far view of "
    cover_page_image2_prompt = "Photo realistic image. Close up view of "
    image_prompt_default = "Photo realistic image of "
    image_prompt_bottom_1 = "Entire image of "
    image_prompt_bottom_2 = " related things close view"