import datetime
from flask import Blueprint
import json

app = Blueprint('filters', __name__, template_folder='templates')


@app.app_template_filter()
def uppercase(text):
    return text.upper()


@app.app_template_filter()
def dateify(date: datetime.date):
    return date.strftime("%B %d, %Y %I:%M %p")


@app.app_template_filter()
def jsonify(text):
    return json.dumps(text, default=str)
