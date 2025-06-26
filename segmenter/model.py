from PIL import Image
import torch

class Segmenter:
    def __init__(self, verbose: bool = True):
        self.expand_ratio = 1.5
        self.model = torch.hub.load(
            'Ramnck/pivo-segmentation',
            'model',
            verbose=verbose,
            pretrained=True,
        )

    def _crop_expanded_bboxes(self, image, boxes, expand_ratio=1.5):
        """
        Crop expanded bounding boxes from a PIL image.

        Args:
            image (PIL.Image): The source image.
            boxes: A list-like object (e.g., a[0].boxes) with .xyxy[i] tensors.
            expand_ratio (float): Expansion factor for the bbox.

        Returns:
            List[PIL.Image]: List of cropped PIL image regions.
        """

        def expand_bbox(bbox, expand_ratio, image_size):
            image_width, image_height = image_size
            x1, y1, x2, y2 = bbox
            w = x2 - x1
            h = y2 - y1
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2

            new_w = w * expand_ratio
            new_h = h * expand_ratio

            new_x1 = max(0, cx - new_w / 2)
            new_y1 = max(0, cy - new_h / 2)
            new_x2 = min(image_width, cx + new_w / 2)
            new_y2 = min(image_height, cy + new_h / 2)

            return [new_x1, new_y1, new_x2, new_y2]
        
        crops = []

        for bbox in boxes:
            b = bbox.xyxy[0]
            b = expand_bbox(b, expand_ratio, image.size)
            x1, y1, x2, y2 = map(int, b)
            cropped = image.crop((x1, y1, x2, y2))
            crops.append(cropped)

        return crops

    # получает изображение с полкой - отдаёт изображения банок
    def segment_image(self, image: Image.Image) -> list[Image.Image]:

        with torch.no_grad():
            output = self.model(image)
            bboxes = output[0].cpu().numpy()

        images = self._crop_expanded_bboxes(image, bboxes.boxes, expand_ratio=self.expand_ratio)

        return images
