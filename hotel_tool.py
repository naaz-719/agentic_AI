
from langchain.tools import tool

@tool
def hotel_recommendation_tool(city: str, min_stars: int = 3, max_price: int = None):
    """Recommend hotels based on city, rating, and price"""
    global hotels_data # Ensure hotels_data is accessible

    results = [
        h for h in hotels_data
        if h["city"].lower() == city.lower()
        and h["stars"] >= min_stars
    ]

    if max_price:
        results = [h for h in results if h["price_per_night"] <= max_price]

    results.sort(key=lambda x: (-x["stars"], x["price_per_night"]))
    return results[:3] if results else {"message": "No hotels found"}
