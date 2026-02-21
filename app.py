import streamlit as st
import json
import os
import sys
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType

# --- 1. RESOLVE LOCAL IMPORTS ---
# This forces Streamlit to see your local files (travel_agent.py, tools, etc.)
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from hotel_tool import hotel_recommendation_tool
    from place_tool import places_discovery_tool
    from weather_tool import weather_lookup_tool
    from budget_tool import budget_estimation_tool
    from final_output import generate_final_output
except ImportError as e:
    st.error(f"❌ Could not load local tools. Ensure all .py files are in: {current_dir}")
    st.stop()

# --- 2. DATA INJECTION ---
def load_json_data():
    """Injects JSON data into the global scope of your tool modules."""
    files = {
        'hotels.json': 'hotel_tool',
        'places.json': 'place_tool'
    }
    for file_name, module_name in files.items():
        path = os.path.join(current_dir, file_name)
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
                # This fixes the 'hotels_data is not defined' error
                sys.modules[module_name].hotels_data = data if 'hotel' in module_name else None
                sys.modules[module_name].places_data = data if 'place' in module_name else None

# --- 3. UI LAYOUT ---
st.set_page_config(page_title="Agentic AI Travel Planner", page_icon="✈️")
st.title("✈️ Agentic AI Travel Assistant")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    st.info("This agent uses LangChain to orchestrate flights, hotels, and weather tools.")

# Input Form
with st.form("travel_form"):
    col1, col2 = st.columns(2)
    with col1:
        source = st.text_input("Source City", "Mumbai")
        days = st.number_input("Trip Duration (Days)", min_value=1, value=3)
    with col2:
        dest = st.text_input("Destination City", "Delhi")
        budget = st.number_input("Total Budget (INR)", min_value=1000, value=25000)
    
    stars = st.slider("Min Hotel Stars", 1, 5, 3)
    submit = st.form_submit_button("Generate Real Itinerary")

# --- 4. AGENT EXECUTION ---
if submit:
    if not api_key:
        st.warning("Please provide an OpenAI API Key in the sidebar.")
    else:
        os.environ["OPENAI_API_KEY"] = api_key
        load_json_data()
        
        with st.spinner(f"🤖 Agent is analyzing {dest} options..."):
            try:
                # Initialize the Real Agent
                llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
                tools = [
                    hotel_recommendation_tool, 
                    places_discovery_tool, 
                    weather_lookup_tool, 
                    budget_estimation_tool
                ]
                
                agent = initialize_agent(
                    tools, 
                    llm, 
                    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                    verbose=True
                )

                # The Prompt that triggers the tools
                query = (f"Plan a {days} day trip to {dest} from {source} with a budget of {budget} INR. "
                         f"Check the weather for {dest} (Lat: 28.6, Lon: 77.2), find {stars}-star hotels, "
                         f"and list the best attractions.")
                
                # Get the agent's reasoned response
                agent_response = agent.run(query)
                
                # Format the output using your final_output logic (modified for strings)
                st.success("✅ Itinerary Generated!")
                st.markdown(f"### 🗺️ Your Personalized Plan for {dest}")
                st.write(agent_response)
                
            except Exception as e:
                st.error(f"Agent Error: {e}")
