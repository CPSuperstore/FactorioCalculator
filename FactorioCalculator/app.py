from flask import Flask, render_template, request
from flask_cors import CORS

import FactorioCalculator.utils as utils
from FactorioCalculator.api import app as api
from FactorioCalculator.filters import app as filters

import FactorioCalculator.factorio_calculator.recipe_manager as recipe_manager

app = Flask(__name__)
cors = CORS(app)

app.register_blueprint(api, url_prefix='/api')

app.register_blueprint(filters)

select_item_page_preload = utils.render_without_request("calculate.twig", recipies=recipe_manager.RECIPE_DATA)


@app.context_processor
def inject_dict_for_all_templates():
    return {
        "development": True
    }


@app.route("/")
def index():
    return render_template("index.twig")


@app.route("/calculate")
def calculate():
    return select_item_page_preload


@app.route("/calculate/<item>")
def calculate_item(item):
    return render_template(
        "calculate_item.twig", item=item, rate=request.args.get("rate", 4, type=int),
        factor=request.args.get("conversionFactor", 60, type=int)
    )


@app.route("/feedback")
def feedback():
    return render_template("feedback.twig")
