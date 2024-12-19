
import os
import uuid
from classes.base import RecipeBook

from PIL import Image, ImageDraw, ImageFont



class Template2RecipebookGenerator(RecipeBook):

    Y_POSITION = 10

    def __init__(self, project_folder, book, template, width = 1000, height = 1200):
        template = self.GENERATOR_MODE_2
        self.Y_POSITION = height // 2 - 330
        super().__init__(project_folder, book)

    def generate_page(self, image1_path, image2_path, image3_path, stopwatch_path, title, title2, time, ingredients, directions, save_path):
        image1, image2, image3, stopwatch = self.load_images(image1_path, image2_path, image3_path, stopwatch_path)
        new_image, draw = self.create_blank_image(800, 1200)
        title_font, title2_font, subtitle_font, text_font = self.define_fonts()
        self.add_title(draw, title, title2, title_font, title2_font, 800)
        self.add_time(draw, stopwatch, time, text_font, new_image, 800)
        self.add_ingredients(draw, ingredients, subtitle_font, text_font, 800)
        self.add_directions(draw, directions, subtitle_font, text_font, 800, 1200)
        self.resize_and_paste_images(draw, new_image, image1, image2, image3, 800, 1200)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        save_path = os.path.join(save_path, str(uuid.uuid4()) + '.png')

        new_image.save(save_path)

    def load_images(self, image1_path, image2_path, image3_path, stopwatch_path):
        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)
        image3 = Image.open(image3_path)
        stopwatch = Image.open(stopwatch_path)
        return image1, image2, image3, stopwatch

    def create_blank_image(self, width, height):
        new_image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(new_image)
        return new_image, draw

    def define_fonts(self):
        title_font = ImageFont.truetype("brushscript.ttf", 60)
        title2_font = ImageFont.truetype("brushscript.ttf", 40)
        subtitle_font = ImageFont.truetype("georgia.ttf", 30)
        text_font = ImageFont.truetype("arial.ttf", 20)
        return title_font, title2_font, subtitle_font, text_font

    def add_title(self, draw, title, title2, title_font, title2_font, width):
            max_width = width - 20
            words = title.split()
            lines = []
            while words:
                line = ''
                while words and draw.textbbox((0, 0), line + words[0], font=title_font)[2] <= max_width:
                    line += (words.pop(0) + ' ')
                lines.append(line)
            for line in lines:
                draw.text((50, self.Y_POSITION), line, font=title_font, fill="black")
                self.Y_POSITION += 40

            words = title2.split()
            self.Y_POSITION += 35
            lines = []
            while words:
                line = ''
                while words and draw.textbbox((0, 0), line + words[0], font=title_font)[2] <= max_width:
                    line += (words.pop(0) + ' ')
                lines.append(line)
            for line in lines:
                draw.text((50, self.Y_POSITION), line, font=title2_font, fill="black")
                self.Y_POSITION += 35

    def add_time(self, draw, stopwatch, time, text_font, new_image, width):
        stopwatch = stopwatch.resize((30, 30))
        self.Y_POSITION += 10
        new_image.paste(stopwatch, (width - 200, self.Y_POSITION))
        self.Y_POSITION += 5

        words = time.split()
        max_width = width
        lines = []
        while words:
            line = ''
            while words and draw.textbbox((0, 0), line + words[0], font=text_font)[2] <= max_width:
                line += (words.pop(0) + ' ')
            lines.append(line)
        for line in lines:
            draw.text((width - 165, self.Y_POSITION), line, font=text_font, fill="black")
            self.Y_POSITION += 30
        

    def add_ingredients(self, draw, ingredients, subtitle_font, text_font, width):
        self.Y_POSITION += 35
        draw.text((75, self.Y_POSITION), "INGREDIENTS", font=subtitle_font, fill="black")
        self.Y_POSITION += 40
        max_width = width // 4 + 50
        for ingredient in ingredients:
            words = ingredient.split()
            lines = []
            while words:
                line = ''
                while words and draw.textbbox((0, 0), line + words[0], font=text_font)[2] <= max_width:
                    line += (words.pop(0) + ' ')
                lines.append(line)
            for line in lines:
                draw.text((75, self.Y_POSITION), line, font=text_font, fill="black")
                self.Y_POSITION += 30

    def add_directions(self, draw, directions, subtitle_font, text_font, width, height):
        draw.text((width // 2 - 50, height // 2 - 120), "DIRECTIONS", font=subtitle_font, fill="black")
        self.Y_POSITION = height // 2 - 80
        max_width = width // 2 + 20
        for i, direction in enumerate(directions):
            direction = f"{i + 1}. {direction}"
            words = direction.split()
            lines = []
            while words:
                line = ''
                while words and draw.textbbox((0, 0), line + words[0], font=text_font)[2] <= max_width:
                    line += (words.pop(0) + ' ')
                lines.append(line)
            for line in lines:
                draw.text((width // 2 - 50, self.Y_POSITION), line, font=text_font, fill="black")
                self.Y_POSITION += 30

    def resize_and_paste_images(self, draw, new_image, image1, image2, image3, width, height):
        line_margin = 65
        draw.line(
            [(line_margin, height // 2 - 150), (width - line_margin, height // 2 - 150)],
            fill="black",
            width=3
        )

        draw.line(
            [(width // 2 - 100, height // 2 - 115), (width // 2 - 100, height // 2 + 425)],
            fill="black",
            width=3
        )
        
        margin = 10
        image3_crop_height = int(image3.height * 0.8)
        image3 = image3.crop((0, image3_crop_height, image3.width, image3.height))
         # Resize images to take half of the page horizontally and vertically
        image1 = image1.resize((width // 2 - 2 * margin, height // 2))
        image2 = image2.resize((width // 2 - 2 * margin, height // 2))
        image3 = image3.resize((image3.width + 155, image3.height))

        # Paste images with margins
        new_image.paste(image1, (margin, -330))
        new_image.paste(image2, (width // 2 + margin, -330))
        new_image.paste(image3, (25, height - image3.height))