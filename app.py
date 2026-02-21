import streamlit as st
import json
import os
import sys

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your custom modules
try:
    from travel_agent import run_travel_agent
    from final_output import generate_final_output
except ImportError as e:
    st.error(f"Failed to import local modules. Ensure travel_agent.py and final_output.py are in the same folder. Error: {e}")

# --- DATA LOADING ---
# Your tools (hotel_tool.py, etc.) expect global variables. 
# We load them here to ensure they are available in the environment.
def load_data():
    try:
        with open('flights.json', 'r') as f:
            import flights_tool # This ensures the tool logic is loaded
            flights_tool.flights_data = json.load(f)
            
        with open('hotels.json', 'r') as f:
            import hotel_tool
            hotel_tool.hotels_data = json.load(f)
            
        with open('places.json', 'r') as f:
            import place_tool
            place_tool.places_data = json.load(f)
        return True
    except FileNotFoundError as e:
        st.error(f"Data file missing: {e}")
        return False

# --- STREAMLIT UI ---
st.set_page_config(page_title="AI Travel Planner", page_icon="🌍", layout="centered")

st.title("✈️ Agentic AI Travel Assistant")
st.markdown("---")

if load_data():
    # Input Form
    with st.form("travel_form"):
        col1, col2 = st.columns(2)
        with col1:
            source = st.text_input("From (Source)", value="Mumbai")
            days = st.number_input("Duration (Nights)", min_value=1, value=3)
        with col2:
            destination = st.text_input("To (Destination)", value="Delhi")
            budget = st.number_input("Budget (INR)", min_value=1000, value=50000)
        
        st.markdown("### Preferences")
        col3, col4 = st.columns(2)
        with col3:
            min_stars = st.slider("Min Hotel Stars", 1, 5, 3)
        with col4:
            p_type = st.selectbox("Attraction Type", ["None", "temple", "park", "museum", "lake", "beach"])

        submit = st.form_submit_button("Generate Itinerary")

    # Execution Logic
    if submit:
        with st.spinner("🤖 Agent is analyzing flights, hotels, and weather..."):
            params = {
                "source": source,
                "destination": destination,
                "days": days,
                "budget": budget,
                "min_hotel_stars": min_stars,
                "place_type": None if p_type == "None" else p_type
            }
            
            try:
                # 1. Trigger the Agentic Logic
                result = run_travel_agent(params)
                
                # 2. Display the Formatted Result
                st.markdown("### 📋 Your Custom Travel Plan")
                formatted_itinerary = generate_final_output(result, days)
                st.info(formatted_itinerary)
                
                # Success indicator
                st.balloons()
                
            except Exception as e:
                st.error(f"Planning failed: {str(e)}")
else:
    st.warning("Please upload flights.json, hotels.json, and places.json to the app directory.")

# Sidebar info
st.sidebar.header("About")
st.sidebar.info("This assistant uses LangChain Agents to query local datasets and external weather APIs to build a budget-conscious travel plan.")
