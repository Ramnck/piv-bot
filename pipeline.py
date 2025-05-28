from segmenter import Segmenter
from classifier import Classifier
from classifier import id_to_label, beer_db
from referrer import Referrer

from pathlib import Path
from PIL import Image

import logging

logger = logging.getLogger(__name__)

segmenter_model = Segmenter()
classifier_model = Classifier()
referrer_model = Referrer()


def process_image(image_path: Path | str, user_prompt: str) -> str:
    shelf_image = Image.open(image_path)
    
    bottles_images = segmenter_model.segment_image(shelf_image)

    bottles_ids_raw = classifier_model.predict_images(bottles_images)
    
    bottle_ids = set(bottles_ids_raw)
    if None in bottle_ids:
        bottle_ids.remove(None)


    bottle_labels = []
    for class_id in bottle_ids:
        if class_id not in id_to_label:
            logger.error(f"NOT EXISTING BOTTLE ID: {class_id}")
        else:
            bottle_labels.append(id_to_label[class_id])

    bottle_infos = []
    for label in bottle_labels:
        if label not in beer_db:
            logger.error(f"NOT EXISTING BOTTLE LABEL: {label}")
        else:
            bottle_infos.append(beer_db[label])
    
    referrence = referrer_model.make_referrence(user_prompt, bottle_infos)

    return referrence
