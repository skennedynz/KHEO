"""
KHEO Energy Model
Version 1.0.0
"""

MONTHS = [
    "Jan", "Feb", "Mar", "Apr",
    "May", "Jun", "Jul", "Aug",
    "Sep", "Oct", "Nov", "Dec"
]

# Steve's annual electricity usage (baseline year)
MONTHLY_USAGE = {
    "Jan": 664,
    "Feb": 583,
    "Mar": 632,
    "Apr": 1005,
    "May": 1564,
    "Jun": 2413,
    "Jul": 2358,
    "Aug": 2488,
    "Sep": 1026,
    "Oct": 1333,
    "Nov": 709,
    "Dec": 635,
}

# Initial Christchurch estimate for a 10.81 kW system.
# These values will later be replaced with a model based on
# irradiance, roof orientation and system efficiency.
MONTHLY_SOLAR = {
    "Jan": 1450,
    "Feb": 1220,
    "Mar": 930,
    "Apr": 650,
    "May": 420,
    "Jun": 310,
    "Jul": 360,
    "Aug": 560,
    "Sep": 820,
    "Oct": 1100,
    "Nov": 1320,
    "Dec": 1480,
}


def monthly_energy_balance():
    """
    Returns a list of monthly energy results.
    """

    results = []

    for month in MONTHS:

        usage = MONTHLY_USAGE[month]
        solar = MONTHLY_SOLAR[month]
        balance = solar - usage

        results.append({
            "month": month,
            "usage": usage,
            "solar": solar,
            "balance": balance,
        })

    return results


def annual_summary():
    """
    Returns annual totals.
    """

    annual_usage = sum(MONTHLY_USAGE.values())
    annual_solar = sum(MONTHLY_SOLAR.values())

    return {
        "usage": annual_usage,
        "solar": annual_solar,
        "balance": annual_solar - annual_usage,
        "coverage": annual_solar / annual_usage,
    }