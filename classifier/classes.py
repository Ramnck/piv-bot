from utils import Info
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    with open(Path(".") / "classifier" / "beer_db.json", encoding="utf-8") as f:
        beer_db_raw = json.load(f)
except Exception as e:
    logger.error(f"ERROR DURING LOADING beer_db.json: {e}")
    exit(1)

beer_db = {i["id"]:Info(**i) for i in beer_db_raw}

# преобразование айдишника классификатора в название пива
id_to_label = {i:j["id"] for i,j in enumerate(beer_db_raw)}