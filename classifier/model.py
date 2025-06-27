from PIL.Image import Image
from transformers import ViTForImageClassification, ViTImageProcessor 
import torch

class Classifier:
    def __init__(self):
        self.confidence = 0.2
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = ViTForImageClassification.from_pretrained("ramnck/beer-classificator").to(self.device)
        self.processor = ViTImageProcessor.from_pretrained("ramnck/beer-classificator")

    # функция возвращает id класса (или None если ошибка)
    def predict_images(self, images: list[Image], with_confidences: bool = False) -> list[int] | list[tuple[int, float]]:

        inputs = self.processor(images, return_tensors="pt")        
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            logits = self.model(**inputs).logits
        probs = torch.softmax(logits, dim=1)

        confidences, labels = probs.max(dim=1)
        confidences, labels = confidences.cpu(), labels.cpu()
        
        mask = confidences > self.confidence
        if with_confidences:
            return list(zip(labels[mask].tolist(), confidences[mask].tolist()))
        else:
            return labels[mask].tolist()
