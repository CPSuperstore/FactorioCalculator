import json
import os

JSON_FILE = "recipes.json"
MACHINES_FILE = "machines.json"

SMELTED_ITEMS = [
    "iron-plate", "copper-plate", "stone-brick", "steel-plate"
]
DRILL_ITEMS = [
    "coal", "stone", "iron-ore", "copper-ore", "uranium-ore"
]
PUMPED_ITEMS = [
    "crude-oil", "water"
]


def read_json_file(filename):
    if not os.path.isfile(filename):
        filename = os.path.join("FactorioCalculator", filename)

    with open(filename) as f:
        return json.loads(f.read())


RECIPE_DATA = read_json_file(JSON_FILE)
MACHINE_DATA = read_json_file(MACHINES_FILE)
