
from langchain.tools import tool

@tool
def budget_estimation_tool(
    flight_price: int,
    hotel_price_per_night: int,
    nights: int,
    daily_local_expense: int = 1500
):
    """Estimate total trip budget"""

    hotel_cost = hotel_price_per_night * nights
    local_cost = daily_local_expense * nights
    total = flight_price + hotel_cost + local_cost

    return {
        "flight_cost": flight_price,
        "hotel_cost": hotel_cost,
        "local_expenses": local_cost,
        "total_budget": total
    }
