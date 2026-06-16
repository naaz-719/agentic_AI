from tools.flight_tool import flight_search_tool
from tools.hotel_tool import hotel_recommendation_tool
from tools.place_tool import places_discovery_tool
from tools.weather_tool import weather_lookup_tool
from tools.budget_tool import budget_estimation_tool

def run_travel_agent(user_query: dict):
    """
    Simple Agentic Controller
    """

    source = user_query["source"]
    destination = user_query["destination"]
    days = user_query["days"]
    budget = user_query.get("budget", None)
    latitude = user_query["latitude"]
    longitude = user_query["longitude"]

    # Flight selection
    flights = flight_search_tool.invoke({
        "source": source,
        "destination": destination
    })
    chosen_flight = flights["cheapest_flight"]

    # Hotel selection
    hotels = hotel_recommendation_tool.invoke({
        "city": destination,
        "min_stars": 3,
        "max_price": budget
    })
    chosen_hotel = hotels[0]

    # Places
    places = places_discovery_tool.invoke({
        "city": destination,
        "min_rating": 4.0
    })

    # Weather
    weather = weather_lookup_tool.invoke({
        "latitude": latitude,
        "longitude": longitude
    })

    # Budget
    cost = budget_estimation_tool.invoke({
        "flight_price": chosen_flight["price"],
        "hotel_price_per_night": chosen_hotel["price_per_night"],
        "nights": days
    })

    # Itinerary
    itinerary = {}
    for day in range(1, days + 1):
        itinerary[f"Day {day}"] = places[(day - 1) % len(places)]["name"]

    return {
        "Flight": chosen_flight,
        "Hotel": chosen_hotel,
        "Weather": weather,
        "Itinerary": itinerary,
        "Estimated Budget": cost
    }
