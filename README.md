# 🗺️ Agentic AI-Based Travel Planning Assistant
An intelligent travel assistant built with LangChain, Python, and Streamlit. Unlike traditional search engines, this assistant uses Agentic AI reasoning to orchestrate multiple tools—analyzing flights, hotels, attractions, and real-time weather—to generate a cohesive, budget-conscious travel itinerary.

# 🚀 Features
- Autonomous Planning: Uses a LangChain Agent to decide which tools to call based on user constraints (budget, city, duration).

- Flight & Hotel Selection: Filters structured local datasets (flights.json, hotels.json) to find the best value options.

- Attraction Discovery: Recommends top-rated points of interest based on user-preferred categories (e.g., beaches, temples).

- Real-time Weather Integration: Connects to the Open-Meteo API to provide live forecasts for the destination.

- Budget Estimation: Automatically calculates total trip costs, including flights, accommodation, and local daily expenses.

# 🛠️ Tech Stack
- Framework: LangChain (Agentic reasoning layer)

- Frontend: Streamlit (Interactive UI)

- LLM: OpenAI GPT (or compatible LangChain LLM)

- Data: JSON-based mock databases for flights, hotels, and places.

- API: Open-Meteo for live weather data.

# 📂 Project Structure

├── app.py                 # Streamlit application (Frontend)
├── travel_agent.py        # Core Agent logic and tool orchestration
├── final_output.py        # Itinerary formatting and output logic
├── budget_tool.py         # Logic for cost estimation
├── hotel_tool.py          # Logic for hotel filtering
├── place_tool.py          # Logic for attraction discovery
├── weather_tool.py        # API connector for weather updates
├── flights.json           # Mock flight data
├── hotels.json            # Mock hotel data
├── places.json            # Mock attractions data
└── requirements.txt       # Project dependencies

# 🤖 How the Agent Works
The system follows a ReAct (Reason + Act) pattern:

- Input: User provides Source, Destination, Budget, and Duration.

- Reasoning: The Agent analyzes the request and decides it first needs flight data, then hotel options within budget.

- Action: Calls flight_tool and hotel_tool.

- Observation: Reviews the data returned by tools.

- Final Output: Compiles a day-wise itinerary using final_output.py.

# 📊 Sample JSON Data Format
The assistant uses structured data like the following for its decision-making:

JSON
{
    "hotel_id": "HOT0001",
    "name": "Grand Palace Hotel",
    "city": "Delhi",
    "stars": 4,
    "price_per_night": 3897,
    "amenities": ["wifi", "pool"]
}

