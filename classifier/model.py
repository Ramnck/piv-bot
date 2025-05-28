from PIL.Image import Image

class Classifier:
    def __init__(self):
        pass

    # функция возвращает id класса (или None если ошибка)
    def predict_image(self, image: Image) -> int | None:
        return 0

    def predict_images(self, images: list[Image]) -> list[int | None]:
        return [self.predict_image(i) for i in images]