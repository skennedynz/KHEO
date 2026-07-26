"""
KHEO Version 1.0.2
energy.py
"""

from pathlib import Path
import csv

# ---------------------------------------------------------------------
# Solar system assumptions
# ---------------------------------------------------------------------

ARRAY_SIZE_KW = 10.81

SYSTEM_EFFICIENCY = 0.86      # 14% losses
SHADING_FACTOR = 0.92         # 8% shading loss

# Monthly solar production factors (sum = 1.0)
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

DATA_FILE = Path("data") / "monthly_usage.csv"


def load_usage():

    usage = []

    with open(DATA_FILE, newline="", encoding="utf-8-sig") as f:

        reader = csv.DictReader(f)

        for row in reader:

            usage.append(
                {
                    "month": row["Month"],
                    "usage": int(row["Usage_kWh"]),
                }
            )

    return usage


def estimated_annual_solar():
    """
    Initial engineering estimate for Christchurch.
    """

    return round(
        ARRAY_SIZE_KW
        * 1300
        * SYSTEM_EFFICIENCY
        * SHADING_FACTOR
    )


def monthly_energy_balance():

    annual_solar = estimated_annual_solar()

    usage = load_usage()

    results = []

    for solar_info, usage_info in zip(MONTHLY_FACTORS, usage):

        month = solar_info[0]
        solar_factor = solar_info[1]

        solar = round(annual_solar * solar_factor)

        demand = usage_info["usage"]

        balance = solar - demand

        results.append(
            {
                "month": month,
                "usage": demand,
                "solar": solar,
                "balance": balance,
            }
        )

    return results


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