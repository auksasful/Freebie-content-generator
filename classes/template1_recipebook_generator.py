
import os
import uuid
from classes.base import Book

from PIL import Image, ImageDraw, ImageFont

class Template1RecipebookGenerator(Book):

    RIGHT_Y_POSITION = 10

    def __init__(self, project_folder, book, template, width = 1000, height = 1200):
        template = self.GENERATOR_MODE_1
        super().__init__(project_folder, book)

    def generate_page(self, image1_path, image2_path, stopwatch_path, title, time, ingredients, directions, save_path, page_number):
        image1, image2, stopwatch = self.load_images(image1_path, image2_path, stopwatch_path)
        new_image, draw = self.create_blank_image(800, 1200)
        title_font, subtitle_font, text_font = self.define_fonts()
        self.add_title(draw, title, title_font, 800)
        self.add_time(draw, stopwatch, time, text_font, new_image, 800)
        self.add_ingredients(draw, ingredients, subtitle_font, text_font, 800)
        self.add_directions(draw, directions, subtitle_font, text_font, 800, 1200)
        self.resize_and_paste_images(new_image, image1, image2, 800, 1200)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        save_path = os.path.join(save_path, str(page_number) + ';' + str(uuid.uuid4()) + '.png')

        new_image.save(save_path)

    def load_images(self, image1_path, image2_path, stopwatch_path):
        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)
        stopwatch = Image.open(stopwatch_path)
        return image1, image2, stopwatch

    def create_blank_image(self, width, height):
        new_image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(new_image)
        return new_image, draw

    def define_fonts(self):
        title_font_path = os.path.join(self.FONTS_PATH, "brushscript.ttf")
        subtitle_font_path = os.path.join(self.FONTS_PATH, "georgia.ttf")
        text_font_path = os.path.join(self.FONTS_PATH, "arial.ttf")

        title_font = ImageFont.truetype(title_font_path, 45)
        subtitle_font = ImageFont.truetype(subtitle_font_path, 30)
        text_font = ImageFont.truetype(text_font_path, 20)
        return title_font, subtitle_font, text_font

    def add_title(self, draw, title, title_font, width):
            max_width = width // 2 - 20
            words = title.split()
            lines = []
            while words:
                line = ''
                while words and draw.textbbox((0, 0), line + words[0], font=title_font)[2] <= max_width:
                    line += (words.pop(0) + ' ')
                lines.append(line)
            for line in lines:
                draw.text((3 * width // 4 - 180, self.RIGHT_Y_POSITION), line, font=title_font, fill="black")
                self.RIGHT_Y_POSITION += 40

    def add_time(self, draw, stopwatch, time, text_font, new_image, width):
        stopwatch = stopwatch.resize((30, 30))
        self.RIGHT_Y_POSITION += 10
        new_image.paste(stopwatch, (3 * width // 4 - 180, self.RIGHT_Y_POSITION))
        self.RIGHT_Y_POSITION += 2

        words = time.split()
        max_width = width // 2 - 50
        lines = []
        while words:
            line = ''
            while words and draw.textbbox((0, 0), line + words[0], font=text_font)[2] <= max_width:
                line += (words.pop(0) + ' ')
            lines.append(line)
        for line in lines:
            draw.text((3 * width // 4 - 145, self.RIGHT_Y_POSITION), line, font=text_font, fill="black")
            self.RIGHT_Y_POSITION += 30
        

    def add_ingredients(self, draw, ingredients, subtitle_font, text_font, width):
        self.RIGHT_Y_POSITION += 10
        draw.text((3 * width // 4 - 180, self.RIGHT_Y_POSITION), "INGREDIENTS", font=subtitle_font, fill="black")
        self.RIGHT_Y_POSITION += 35
        max_width = width // 2 - 30
        for ingredient in ingredients:
            words = ingredient.split()
            lines = []
            while words:
                line = ''
                while words and draw.textbbox((0, 0), line + words[0], font=text_font)[2] <= max_width:
                    line += (words.pop(0) + ' ')
                lines.append(line)
            for line in lines:
                draw.text((3 * width // 4 - 180, self.RIGHT_Y_POSITION), line, font=text_font, fill="black")
                self.RIGHT_Y_POSITION += 30

    def add_directions(self, draw, directions, subtitle_font, text_font, width, height):
        draw.text((20, height - 590), "DIRECTIONS", font=subtitle_font, fill="black")
        y_position = height - 540
        max_width = width // 2 - 20
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
                draw.text((20, y_position), line, font=text_font, fill="black")
                y_position += 30

    def resize_and_paste_images(self, new_image, image1, image2, width, height):
        image1 = image1.resize((width // 2, height // 2))
        image2 = image2.resize((width // 2, height // 2))
        new_image.paste(image1, (0, 0))
        new_image.paste(image2, (width // 2, height // 2))