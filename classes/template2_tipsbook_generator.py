
import os
import uuid
from classes.base import Book

from PIL import Image, ImageDraw, ImageFont



class Template2TipsbookGenerator(Book):

    Y_POSITION = 10

    def __init__(self, project_folder, book, template, width = 1000, height = 1200):
        template = self.GENERATOR_MODE_2
        self.Y_POSITION = height // 2 - 330
        super().__init__(project_folder, book)

    def generate_page(self, image1_path, image2_path, image3_path, title, title2, description, instructions, save_path, page_number):
        image1, image2, image3 = self.load_images(image1_path, image2_path, image3_path)
        new_image, draw = self.create_blank_image(800, 1200)
        title_font, title2_font, subtitle_font, text_font = self.define_fonts()
        self.add_title(draw, title, title2, title_font, title2_font, 800)
        self.add_description(draw, description, subtitle_font, text_font, 800, 1200)
        self.add_instructions(draw, instructions, subtitle_font, text_font, 800, 1200)
        self.resize_and_paste_images(draw, new_image, image1, image2, image3, 800, 1200)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        save_path = os.path.join(save_path, str(page_number) + ';' + str(uuid.uuid4()) + '.png')

        new_image.save(save_path)

    def load_images(self, image1_path, image2_path, image3_path):
        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)
        image3 = Image.open(image3_path)
        return image1, image2, image3

    def create_blank_image(self, width, height):
        new_image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(new_image)
        return new_image, draw

    def define_fonts(self):
        title_font_path = os.path.join(self.FONTS_PATH, "brushscript.ttf")
        subtitle_font_path = os.path.join(self.FONTS_PATH, "georgia.ttf")
        text_font_path = os.path.join(self.FONTS_PATH, "arial.ttf")
        title_font = ImageFont.truetype(title_font_path, 60)
        title2_font = ImageFont.truetype(title_font_path, 40)
        subtitle_font = ImageFont.truetype(subtitle_font_path, 30)
        text_font = ImageFont.truetype(text_font_path, 20)
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
        

    def add_description(self, draw, description, subtitle_font, text_font, width, height):
        self.Y_POSITION = height // 2 - 120
        draw.text((75, self.Y_POSITION), "DESCRIPTION", font=subtitle_font, fill="black")
        self.Y_POSITION += 40
        max_width = width // 4 + 15
        words = description.split()
        lines = []
        while words:
            line = ''
            while words and draw.textbbox((0, 0), line + words[0], font=text_font)[2] <= max_width:
                line += (words.pop(0) + ' ')
            lines.append(line)
        for line in lines:
            draw.text((75, self.Y_POSITION), line, font=text_font, fill="black")
            self.Y_POSITION += 30

    def add_instructions(self, draw, directions, subtitle_font, text_font, width, height):
        draw.text((width // 2 - 50, height // 2 - 120), "INSTRUCTIONS", font=subtitle_font, fill="black")
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