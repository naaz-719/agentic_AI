import streamlit as st
import json
import os
import sys

# --- STEP 1: FIX PATH ISSUES ---
# This ensures Streamlit looks in the current folder for your uploaded .py files
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# --- STEP 2: ATTEMPT IMPORTS ---
try:
    from travel_agent import run_travel_agent
    from final_output import generate_final_output
    import hotel_tool
    import place_tool
    # If you have a flights_tool.py, import it; otherwise we'll handle data locally
    try:
        import flights_tool
    except ImportError:
        flights_tool = None
except ImportError as e:
    st.error(f"❌ Critical Error: Missing Python files in directory. {e}")
    st.stop()

# --- STEP 3: ROBUST DATA LOADING ---
def initialize_data():
    """Loads JSON data and injects it into the tool modules' global scope."""
    data_files = {
        'flights.json': 'flights_data',
        'hotels.json': 'hotels_data',
        'places.json': 'places_data'
    }
    
    success = True
    for file_name, var_name in data_files.items():
        file_path = os.path.join(current_dir, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
                # Inject data into the specific tool modules where they are expected
                if file_name == 'hotels.json':
                    hotel_tool.hotels_data = data
                elif file_name == 'places.json':
                    place_tool.places_data = data
                elif file_name == 'flights.json' and flights_tool:
                    flights_tool.flights_data = data
        else:
            st.warning(f"⚠️ Missing file: {file_name}")
            success = False
    return success

# --- STEP 4: UI DESIGN ---
st.set_page_config(page_title="AI Travel Planner", page_icon="✈️")

st.title("✈️ Agentic AI Travel Assistant")
st.sidebar.header("Navigation & Info")
st.sidebar.info("This agent uses LangChain to orchestrate flights, hotels, and weather tools.")

data_loaded = initialize_data()

if not data_loaded:
    st.error("Missing JSON datasets. Please ensure flights.json, hotels.json, and places.json are in the app folder.")
    st.stop()

# User Input Form
with st.form("planner_form"):
    col1, col2 = st.columns(2)
    with col1:
        source = st.text_input("Source City", value="Mumbai")
        days = st.number_input("Trip Duration (Nights)", min_value=1, value=3)
    with col2:
        destination = st.text_input("Destination City", value="Delhi")
        budget = st.number_input("Total Budget (INR)", min_value=1000, value=20000)
    
    st.markdown("---")
    col3, col4 = st.columns(2)
    with col3:
        min_stars = st.slider("Min Hotel Rating", 1, 5, 3)
    with col4:
        p_type = st.selectbox("Attraction Preference", ["None", "temple", "park", "museum", "lake", "beach"])

    submit_button = st.form_submit_button("Generate My Itinerary")

# --- STEP 5: EXECUTION ---
if submit_button:
    with st.spinner(f"🤖 Agent is searching for the best deals in {destination}..."):
        # Prepare params
        travel_params = {
            "source": source,
            "destination": destination,
            "days": days,
            "budget": budget,
            "min_hotel_stars": min_stars,
            "place_type": None if p_type == "None" else p_type
        }
        
        try:
            # Call the agent logic from travel_agent.py
            agent_response = run_travel_agent(travel_params)
            
            # Format using final_output.py
            itinerary_text = generate_final_output(agent_response, days)
            
            st.success("✅ Itinerary Generated Successfully!")
            st.markdown(itinerary_text)
            
        except Exception as e:
            st.error(f"An error occurred during planning: {e}")
            
