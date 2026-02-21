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
