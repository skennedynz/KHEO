"""
KHEO Version 1.0.4
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
SOLAR_FILE = DATA_FOLDER / "monthly_solar.csv"

# ---------------------------------------------------------------------
# Load monthly solar factors
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Load monthly solar resource
# ---------------------------------------------------------------------

def load_monthly_solar():

    solar = []

    with open(SOLAR_FILE, newline="", encoding="utf-8-sig") as f:

        reader = csv.DictReader(f)

        for row in reader:

            solar.append(
                {
                    "month": row["Month"],
                    "days": int(row["Days"]),
                    "psh": float(row["Peak_Sun_Hours"]),
                }
            )

    return solar

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
# Monthly energy balance
# ---------------------------------------------------------------------

def monthly_energy_balance():

    parameters = load_parameters()

    # Calculate total array size from panel configuration
    ne_array_kw = (
        parameters["NE_Panels"]
        * parameters["Panel_Rating_kW"]
    )

    nw_array_kw = (
        parameters["NW_Panels"]
        * parameters["Panel_Rating_kW"]
    )

    total_array_kw = ne_array_kw + nw_array_kw

    usage = load_usage()
    solar_resource = load_monthly_solar()

    results = []

    for solar_month, item in zip(solar_resource, usage):

        month = solar_month["month"]
        days = solar_month["days"]
        psh = solar_month["psh"]

        solar = round(
            total_array_kw
            * psh
            * days
            * parameters["System_Efficiency"]
            * parameters["Shading_Factor"]
        )

        demand = item["usage"]

        direct_use = round(
            solar * parameters["Direct_Solar_Use"]
        )

        grid_export = max(0, solar - direct_use)

        grid_import = max(0, demand - direct_use)

        balance = solar - demand

        results.append(
            {
                "month": month,
                "usage": demand,
                "solar": solar,
                "direct_use": direct_use,
                "grid_import": grid_import,
                "grid_export": grid_export,
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