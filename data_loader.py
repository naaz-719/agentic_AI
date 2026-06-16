import json
from pathlib import Path
import os

try:
    BASE_DIR = Path(__file__).resolve().parent.parent
except NameError:
    BASE_DIR = Path(os.getcwd())

DATA_DIR = BASE_DIR / "Data_Sources"

def load_json(filename: str):
    file_path = DATA_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} not found")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

flights_data = load_json("flights.json")
hotels_data = load_json("hotels.json")
places_data = load_json("places.json")
