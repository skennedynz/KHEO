"""
KHEO Version 2.0.0
solar.py
"""

from pathlib import Path
import csv

DATA_FOLDER = Path("data")

ROOF_FILE = DATA_FOLDER / "roof_geometry.csv"
SOLAR_FILE = DATA_FOLDER / "solar_resource.csv"


def load_roof_geometry():

    roofs = []

    with open(ROOF_FILE, newline="", encoding="utf-8-sig") as f:

        reader = csv.DictReader(f)

        for row in reader:

            roofs.append(
                {
                    "roof": row["Roof"],
                    "panels": int(row["Panels"]),
                    "panel_rating": float(row["Panel_Rating_kW"]),
                    "tilt": float(row["Tilt_deg"]),
                    "azimuth": float(row["Azimuth_deg"]),
                }
            )

    return roofs


def load_solar_resource():

    resource = []

    with open(SOLAR_FILE, newline="", encoding="utf-8-sig") as f:

        reader = csv.DictReader(f)

        for row in reader:

            resource.append(
                {
                    "month": row["Month"],
                    "days": int(row["Days"]),
                    "psh": float(row["PSH"]),
                }
            )

    return resource

def total_array_capacity():

    total_kw = 0.0

    for roof in load_roof_geometry():

        total_kw += (
            roof["panels"]
            * roof["panel_rating"]
        )

    return total_kw

def load_model_parameters():

    parameters = {}

    MODEL_FILE = DATA_FOLDER / "model_parameters.csv"

    with open(MODEL_FILE, newline="", encoding="utf-8-sig") as f:

        reader = csv.DictReader(f)

        for row in reader:

            parameters[row["Parameter"]] = float(row["Value"])

    return parameters