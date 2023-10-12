from PIL import Image
from io import BytesIO
import os
from pathlib import Path


class GenerateVS:
    def __init__(self, image1, image2):
        self.image1 = image1
        self.image2 = image2
        self.path = os.path.join(Path(__file__).parent, "images")
        self.portrait1 = Image.open(BytesIO(image1))
        self.portrait2 = Image.open(BytesIO(image2))
        self.vs_icon = Image.open(os.path.join(self.path, "vs_icon.png"))
        self.crown = Image.open(os.path.join(self.path, "crown.png"))
        self.width, self.height = self.portrait1.size
        self.new_image = Image.new("RGBA", (768, 256), (0, 0, 0, 0))

    def delete_images(self) -> bool:
        os.remove(os.path.join(self.path, "vs.png"))
        # os.remove(os.path.join(self.path, "win.png"))
        return True

    def generate_vs_image(self) -> str:
        width, height = self.portrait1.size
        vs_icon_resize = self.vs_icon.resize((width, height))
        self.new_image.paste(
            self.portrait1, (0, 0)
        )  # Paste the third image on the left
        self.new_image.paste(
            vs_icon_resize, (width, 0)
        )  # Paste the second image in the middle
        self.new_image.paste(self.portrait2, (2 * width, 0))
        save_path = os.path.join(self.path, "vs.png")
        self.new_image.save(save_path)
        return save_path

    def generate_win_image(self) -> str:
        ...
