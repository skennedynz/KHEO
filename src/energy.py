"""
KHEO Version 1.0.1
energy.py
"""

# Annual house electricity usage (kWh)
ANNUAL_USAGE = 16686

# Solar system
ARRAY_SIZE_KW = 10.81

# Editable engineering assumptions
SYSTEM_EFFICIENCY = 0.86      # 14% total system losses
SHADING_FACTOR = 0.92         # 8% shading loss

# Monthly production factors
# Sum = 1.000
MONTHLY_FACTORS = [
    ("Jan", 0.124),
    ("Feb", 0.112),
    ("Mar", 0.098),
    ("Apr", 0.078),
    ("May", 0.053),
    ("Jun", 0.039),
    ("Jul", 0.045),
    ("Aug", 0.063),
    ("Sep", 0.084),
    ("Oct", 0.101),
    ("Nov", 0.105),
    ("Dec", 0.098),
]

# Monthly house usage profile
# Sum = 1.000
USAGE_FACTORS = [
    0.095,
    0.085,
    0.080,
    0.075,
    0.080,
    0.090,
    0.100,
    0.095,
    0.080,
    0.075,
    0.070,
    0.075,
]


def estimated_annual_solar():
    """
    First-pass engineering estimate.

    Assumes approximately 1,300 kWh per installed kW per year
    for a well-oriented Christchurch residential system.
    """

    return round(
        ARRAY_SIZE_KW
        * 1300
        * SYSTEM_EFFICIENCY
        * SHADING_FACTOR
    )


def monthly_energy_balance():

    annual_solar = estimated_annual_solar()

    results = []

    total_usage = 0
    total_solar = 0

    for (month, solar_factor), usage_factor in zip(
        MONTHLY_FACTORS,
        USAGE_FACTORS,
    ):

        usage = round(ANNUAL_USAGE * usage_factor)
        solar = round(annual_solar * solar_factor)
        balance = solar - usage

        total_usage += usage
        total_solar += solar

        results.append(
            {
                "month": month,
                "usage": usage,
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