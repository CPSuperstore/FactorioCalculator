import math
import typing

from FactorioCalculator.data_structures import Recipe
from FactorioCalculator.models import ProductionType

import FactorioCalculator.factorio_calculator.recipe_manager as recipe_manager


def get_data(item: str):
    return recipe_manager.RECIPE_DATA[item]["recipe"]


def generate_hierarchy(item):
    d = get_data(item)

    tree = Recipe(item, d["time"], d["yield"], None)
    tree = build_tree(tree)

    return tree


def build_tree(parent: Recipe):
    recipe = get_data(parent.item)

    for i in recipe["ingredients"]:
        d = get_data(i["id"])
        ingredient = Recipe(i["id"], d["time"], d["yield"], i["amount"])

        parent.add_ingredients(ingredient)
        build_tree(ingredient)

    return parent


def calculate_hierarchy(hierarchy: Recipe, rate: int, assembly_machine="3", furnace="electric", drill="electric", pump="pumpjack"):
    recursive_hierarchy_calculation(hierarchy, rate, assembly_machine, furnace, drill, pump)
    calculate_node(hierarchy, rate, assembly_machine, furnace, drill, pump, recurse=False)


def calculate_node(
        ingredient: Recipe, rate: int, assembly_machine="3", furnace="electric", drill="electric", pump="pumpjack",
        recurse=True
):

    if ingredient.item in ["water"]:
        ingredient.machines_needed = 1

    else:
        s = recipe_manager.MACHINE_DATA[ingredient.production_type.value][
            locals()[ingredient.production_type.value.replace("-", "_")]]["speed"]

        i = ingredient.quantity_required if ingredient.quantity_required is not None else 1

        if ingredient.production_type in [ProductionType.MINING_DRILL, ProductionType.PUMP]:
            ingredient.machines_needed = (rate * i) / s
        else:
            ingredient.machines_needed = ((rate * i) * ingredient.time) / (ingredient.output * s)

        ingredient.machines_needed = round(ingredient.machines_needed, 2)
    if recurse:
        calculate_hierarchy(ingredient, rate, assembly_machine, furnace, drill, pump)


def recursive_hierarchy_calculation(hierarchy: Recipe, rate: int, assembly_machine="3", furnace="electric", drill="electric", pump="pumpjack"):
    for ingredient in hierarchy.ingredients:        # type: Recipe
        calculate_node(ingredient, rate, assembly_machine, furnace, drill, pump)


def count_components(hierarchy: Recipe, data=None, round_numbers=True):
    if data is None:
        data = {}

    if hierarchy.production_type not in data:
        data[hierarchy.production_type] = 0

    if round_numbers:
        n = math.ceil(hierarchy.machines_needed)
    else:
        n = hierarchy.machines_needed
    data[hierarchy.production_type] += n

    for i in hierarchy.ingredients:
        data = count_components(i, data, round_numbers)

    return data


def estimate_value(counts: typing.Dict[ProductionType, float], mode, assembly_machine="3", furnace="electric", drill="electric", pump="pumpjack"):
    rs = {}
    total = 0

    for production_type, count in counts.items():
        t = recipe_manager.MACHINE_DATA[production_type.value][
        locals()[production_type.value.replace("-", "_")]][mode] * count
        rs[production_type] = t
        total += t

    return total, rs