from PIL import Image

class Segmenter:
    def __init__(self):
        pass

    # получает изображение с полкой - отдаёт изображения банок
    def segment_image(self, image: Image.Image) -> list[Image.Image]:
        return [Image.new(mode="RGB", size=(200, 200), color=(255, 255, 255))]
