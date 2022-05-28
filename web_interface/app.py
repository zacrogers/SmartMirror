from html import entities
from flask import Flask, render_template
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import City, Country

app = Flask(__name__)

PATH = os.path.dirname(os.path.realpath(__file__))


@app.route("/")
def index():
    settings = {}
    with open(f"{PATH}/settings.json", "r") as json_file:
        settings = json.load(json_file)

    current_country = settings.get("country")
    current_city = settings.get("city")
    entities = settings.get("hass_entities", {})

    valid_cities = City.to_dict()
    valid_countries = Country.to_dict()

    return render_template(
        "index.html",
        sensor_entities=entities,
        current_city=current_city,
        current_country=current_country,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
