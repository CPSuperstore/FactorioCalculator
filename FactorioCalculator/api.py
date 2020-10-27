from flask import Blueprint, request, jsonify
import time
from FactorioCalculator.factorio_calculator import recipe_hierarchy as recipe_hierarchy
from FactorioCalculator.factorio_calculator import recipe_manager as recipe_manager

app = Blueprint('api', __name__, template_folder='templates')


@app.route("/calculate")
def calculate():
    item = request.args.get("item")
    rate = request.args.get("rate", type=int)
    factor = request.args.get("conversionFactor", type=float)
    rate = rate / factor

    hierarchy = recipe_hierarchy.generate_hierarchy(item)
    recipe_hierarchy.calculate_hierarchy(hierarchy, rate)

    counts = recipe_hierarchy.count_components(hierarchy)
    total_energy, energy = recipe_hierarchy.estimate_value(counts, "energy")
    total_pollution, pollution = recipe_hierarchy.estimate_value(counts, "pollution")

    result = {
        "hierarchy": hierarchy.generate_dict(),
        "machineCounts": counts,
        "energy": energy,
        "pollution": pollution,
        "totalEnergy": total_energy,
        "totalPollution": total_pollution
    }

    for key in ["machineCounts", "energy", "pollution"]:
        d = {}
        for k, v in result[key].items():
            d[k.value] = v

        result[key] = d

    result["item"] = recipe_manager.RECIPE_DATA[item]
    result["rate"] = rate

    return jsonify(result)
