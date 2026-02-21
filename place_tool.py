
from langchain.tools import tool

@tool
def places_discovery_tool(city: str, place_type: str = None, min_rating: float = 4.0):
    """Recommend attractions based on type and rating"""
    global places_data # Ensure places_data is accessible

    results = [
        p for p in places_data
        if p["city"].lower() == city.lower()
        and p["rating"] >= min_rating
    ]

    if place_type:
        results = [p for p in results if p["type"].lower() == place_type.lower()]

    results.sort(key=lambda x: -x["rating"])
    return results[:5] if results else {"message": "No attractions found"}
