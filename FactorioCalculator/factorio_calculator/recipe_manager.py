import json

JSON_URL = "https://kevinta893.github.io/factorio-recipes-json/recipes.dictionary.json"
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


def get_recipes():
    with open(JSON_FILE) as f:
        return json.loads(f.read())


def get_machines():
    with open(MACHINES_FILE) as f:
        return json.loads(f.read())


RECIPE_DATA = get_recipes()
MACHINE_DATA = get_machines()
