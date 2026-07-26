"""
KHEO Version 1.0.3
energy.py
"""

from pathlib import Path
import csv

# ---------------------------------------------------------------------
# Data files
# ---------------------------------------------------------------------

DATA_FOLDER = Path("data")

USAGE_FILE = DATA_FOLDER / "monthly_usage.csv"
PARAMETER_FILE = DATA_FOLDER / "system_parameters.csv"


# ---------------------------------------------------------------------
# Load engineering parameters
# ---------------------------------------------------------------------

def load_parameters():

    parameters = {}

    with open(PARAMETER_FILE, newline="", encoding="utf-8-sig") as f:

        reader = csv.DictReader(f)

        for row in reader:

            value = row["Value"]

            try:
                value = float(value)
            except ValueError:
                pass

            parameters[row["Parameter"]] = value

    return parameters


# ---------------------------------------------------------------------
# Load measured monthly usage
# ---------------------------------------------------------------------

def load_usage():

    usage = []

    with open(USAGE_FILE, newline="", encoding="utf-8-sig") as f:

        reader = csv.DictReader(f)

        for row in reader:

            usage.append(
                {
                    "month": row["Month"],
                    "usage": int(row["Usage_kWh"]),
                }
            )

    return usage


# ---------------------------------------------------------------------
# Monthly solar distribution
# ---------------------------------------------------------------------

MONTHLY_FACTORS = [
    ("Apr", 0.078),
    ("May", 0.053),
    ("Jun", 0.039),
    ("Jul", 0.045),
    ("Aug", 0.063),
    ("Sep", 0.084),
    ("Oct", 0.101),
    ("Nov", 0.105),
    ("Dec", 0.098),
    ("Jan", 0.124),
    ("Feb", 0.112),
    ("Mar", 0.098),
]


# ---------------------------------------------------------------------
# Solar model
# ---------------------------------------------------------------------

def estimated_annual_solar():

    parameters = load_parameters()

    return round(
        parameters["Array_Size_kW"]
        * 1300
        * parameters["System_Efficiency"]
        * parameters["Shading_Factor"]
    )


# ---------------------------------------------------------------------
# Monthly energy balance
# ---------------------------------------------------------------------

def monthly_energy_balance():

    parameters = load_parameters()

    annual_solar = round(
        parameters["Array_Size_kW"]
        * 1300
        * parameters["System_Efficiency"]
        * parameters["Shading_Factor"]
    )

    usage = load_usage()

    results = []

    for (month, factor), item in zip(MONTHLY_FACTORS, usage):

        solar = round(annual_solar * factor)

        demand = item["usage"]

        direct_use = round(
            solar * parameters["Direct_Solar_Use"]
        )

        export = max(0, solar - direct_use)

        grid_import = max(0, demand - direct_use)

        balance = solar - demand

        results.append(
            {
                "month": month,
                "usage": demand,
                "solar": solar,
                "direct_use": direct_use,
                "grid_import": grid_import,
                "grid_export": export,
                "balance": balance,
            }
        )

    return results


# ---------------------------------------------------------------------
# Annual summary
# ---------------------------------------------------------------------

def annual_summary():

    monthly = monthly_energy_balance()

    usage = sum(m["usage"] for m in monthly)
    solar = sum(m["solar"] for m in monthly)
    balance = solar - usage

    coverage = solar / usage if usage else 0

    return {
        "usage": usage,
        "solar": solar,
        "balance": balance,
        "coverage": coverage,
    }