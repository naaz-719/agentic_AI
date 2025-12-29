import json
import pyttsx3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

DATA_PATH = "data"

def load_flights():
    with open(f"{DATA_PATH}/flights.json","r") as f:
        return json.load(f)

def load_hotels():
    with open(f"{DATA_PATH}/hotels.json","r") as f:
        return json.load(f)

def load_places():
    with open(f"{DATA_PATH}/places.json","r") as f:
        return json.load(f)

FLIGHTS = load_flights()
HOTELS = load_hotels()
PLACES = load_places()


# ---------- DIRECT FLIGHTS ----------
def search_flights(source, destination):
    result = [
        f for f in FLIGHTS
        if f["from"].lower() == source.lower() and f["to"].lower() == destination.lower()
    ]
    return sorted(result, key=lambda x: x["price"])


# ---------- VIA FLIGHTS ----------
def search_via_flights(source, destination):
    via_options = []

    for f1 in FLIGHTS:
        for f2 in FLIGHTS:
            if (
                f1["from"].lower() == source.lower()
                and f2["to"].lower() == destination.lower()
                and f1["to"].lower() == f2["from"].lower()
            ):
                via_options.append({
                    "via_city": f1["to"],
                    "first_leg": f1,
                    "second_leg": f2,
                    "total_price": f1["price"] + f2["price"]
                })

    return sorted(via_options, key=lambda x: x["total_price"])


# ---------- HOTELS ----------
def search_hotels(city):
    result = [h for h in HOTELS if h["city"].lower() == city.lower()]
    return sorted(result, key=lambda x: x["price_per_night"])


# ---------- PLACES ----------
def search_places(city):
    return [p for p in PLACES if p["city"].lower() == city.lower()]


# ---------- ITINERARY ----------
def build_itinerary(city, days, preference=None):
    places = search_places(city)

    if preference:
        places = [p for p in places if p["category"].lower() == preference.lower()]

    places = sorted(places, key=lambda x: x["rating"], reverse=True)

    itinerary = {}
    i = 0

    for d in range(1, days+1):
        itinerary[f"Day {d}"] = []
        for _ in range(3):
            if i < len(places):
                itinerary[f"Day {d}"].append(places[i]["name"])
                i += 1

    return itinerary


# ---------- BUDGET ----------
def calculate_budget(flight, hotel_cost, days):
    return {
        "flight_cost": flight,
        "hotel_total": hotel_cost * days,
        "local_expenses": 1500 * days,
        "total": flight + hotel_cost*days + 1500*days
    }


# ---------- PDF ----------
def generate_pdf(result, path):
    c = canvas.Canvas(path, pagesize=letter)
    text = c.beginText(40, 750)

    text.textLine("AI Travel Plan")
    text.textLine("-----------------------")
    text.textLine(result["summary"])
    text.textLine("")

    text.textLine("Budget")
    text.textLine(str(result["budget"]))

    text.textLine("")
    text.textLine("Itinerary")

    for d, p in result["itinerary"].items():
        text.textLine(f"{d}: {', '.join(p)}")

    c.drawText(text)
    c.save()


# ---------- VOICE ----------
def speak_budget(result):
    engine = pyttsx3.init()
    engine.say(f"Your total budget is {result['total']} rupees")
    engine.runAndWait()
