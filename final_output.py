

from datetime import datetime, timedelta

# -------------------------------------------------
# Function 1: Generate structured final output
# -------------------------------------------------
def generate_final_output(agent_result: dict, days: int):
    flight = agent_result["Flight"]
    hotel = agent_result["Hotel"]
    itinerary = agent_result["Itinerary"]
    weather = agent_result["Weather"]
    budget = agent_result["Estimated Budget"]

    trip_summary = {
        "From": flight["from"],
        "To": flight["to"],
        "Duration": f"{days} Days",
        "Travel Mode": "Flight",
        "Hotel Category": f"{hotel['stars']}-Star"
    }

    flight_details = {
        "Airline": flight["airline"],
        "Departure": flight["departure_time"],
        "Arrival": flight["arrival_time"],
        "Duration": flight["duration_hours"],
        "Price": flight["price"]
    }

    hotel_details = {
        "Hotel Name": hotel["name"],
        "City": hotel["city"],
        "Stars": hotel["stars"],
        "Price Per Night": hotel["price_per_night"],
        "Amenities": hotel["amenities"]
    }

    start_date = datetime.today()
    day_plan = {}

    for i, (day, place) in enumerate(itinerary.items()):
        day_plan[day] = {
            "Date": (start_date + timedelta(days=i)).strftime("%Y-%m-%d"),
            "Activity": place
        }

    weather_forecast = {}
    for day in day_plan:
        weather_forecast[day] = {
            "Max Temp": weather["max_temp"],
            "Min Temp": weather["min_temp"],
            "Wind Speed": weather["wind_speed"]
        }

    budget_breakdown = {
        "Flight Cost": budget["flight_cost"],
        "Hotel Cost": budget["hotel_cost"],
        "Local Expenses": budget["local_expenses"],
        "Total Estimated Budget": budget["total_budget"]
    }

    return {
        "Trip Summary": trip_summary,
        "Flight Option Selected": flight_details,
        "Hotel Recommendation": hotel_details,
        "Day-wise Itinerary": day_plan,
        "Weather Forecast": weather_forecast,
        "Budget Breakdown": budget_breakdown
    }


# -------------------------------------------------
# Function 2: Print Expected Results (Human Readable)
# -------------------------------------------------
def print_expected_results(final_output: dict):
    trip = final_output["Trip Summary"]
    flight = final_output["Flight Option Selected"]
    hotel = final_output["Hotel Recommendation"]
    itinerary = final_output["Day-wise Itinerary"]
    weather = final_output["Weather Forecast"]
    budget = final_output["Budget Breakdown"]

    print("=" * 45)
    print(f"Your {trip['Duration']} Trip to {trip['To']}")
    print("=" * 45)

    print("\n✈️ Flight Selected:")
    print(
        f"- {flight['Airline']} (₹{flight['Price']}) – "
        f"Departs {trip['From']} at {flight['Departure'][11:16]}"
    )

    print("\n🏨 Hotel Booked:")
    print(
        f"- {hotel['Hotel Name']} "
        f"(₹{hotel['Price Per Night']}/night, {hotel['Stars']}-star)"
    )

    print("\n🌦️ Weather:")
    for day, info in weather.items():
        print(
            f"- {day}: Max {info['Max Temp']}°C, "
            f"Min {info['Min Temp']}°C"
        )

    print("\n🗺️ Itinerary:")
    for day, details in itinerary.items():
        print(f"{day}: {details['Activity']}")

    print("\n💰 Estimated Total Budget:")
    print(f"- Flight: ₹{budget['Flight Cost']}")
    print(f"- Hotel: ₹{budget['Hotel Cost']}")
    print(f"- Food & Travel: ₹{budget['Local Expenses']}")
    print("-" * 37)
    print(f"Total Cost: ₹{budget['Total Estimated Budget']}")

    print("=" * 45)
