from FactorioCalculator.models import ProductionType

import FactorioCalculator.factorio_calculator.recipe_manager as recipe_manager


class Recipe:
    def __init__(self, item, time, output, quantity_required):
        self.ingredients = []

        self.item = item                                                # type: str
        self.time = time                                                # type: float
        self.output = output                                            # type: int
        self.quantity_required = quantity_required                      # type: int
        self.parent = None
        self.machines_needed = None                                     # type: int

        self.production_type = ProductionType.ASSEMBLING_MACHINE        # type: ProductionType
        if item in recipe_manager.DRILL_ITEMS:
            self.production_type = ProductionType.MINING_DRILL
        elif item in recipe_manager.SMELTED_ITEMS:
            self.production_type = ProductionType.FURNACE
        elif item in recipe_manager.PUMPED_ITEMS:
            self.production_type = ProductionType.PUMP

    def set_parent(self, p):
        self.parent = p
        self.quantity_required *= p.quantity_required if p.quantity_required is not None else 1

    def add_ingredients(self, tree):
        tree.set_parent(self)
        self.ingredients.append(tree)

    def __repr__(self):
        i = self.item + "({})".format(self.machines_needed)
        if len(self.ingredients) == 0:
            return i

        return i + ": " + str(self.ingredients)

    def generate_dict(self):
        return {
            self.item: {
                "count": self.machines_needed,
                "processor": self.production_type.value,
                "resources": self.dict(),
            }
        }


    def dict(self, data=None):
        if data is None:
            data = {}

        for i in self.ingredients:
            data[i.item] = {
                "count": i.machines_needed,
                "processor": i.production_type.value,
                "resources": i.dict(),
            }

        return data
