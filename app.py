import streamlit as st
from travel_agent import run_travel_agent
from final_output import generate_final_output

# Set up page configuration
st.set_page_config(page_title="Agentic AI Travel Planner", page_icon="✈️", layout="wide")

# App Header
st.title("🗺️ Agentic AI-Based Travel Planning Assistant")
st.markdown("""
This assistant uses **LangChain Agents** to help you plan your perfect trip. 
It analyzes flights, suggests hotels, discovers attractions, and checks the weather to build a custom itinerary.
""")

# Sidebar for User Inputs
with st.sidebar:
    st.header("Trip Details")
    source = st.text_input("Source City", placeholder="e.g., Bangalore")
    destination = st.text_input("Destination City", placeholder="e.g., Goa")
    
    col1, col2 = st.columns(2)
    with col1:
        days = st.number_input("Duration (Days)", min_value=1, max_value=30, value=3)
    with col2:
        budget = st.number_input("Budget ($)", min_value=100, value=1000)

    # Additional preferences
    hotel_rating = st.slider("Min Hotel Rating (Stars)", 1, 5, 3)
    attraction_type = st.selectbox("Preferred Attraction Type", ["None", "beach", "temple", "park", "museum", "lake"])
    
    plan_trip = st.button("Generate Travel Plan")

# Main Content Area
if plan_trip:
    if not source or not destination:
        st.error("Please enter both a source and destination city.")
    else:
        with st.spinner(f"Agent is reasoning and planning your trip to {destination}..."):
            # Prepare parameters for the agent
            travel_params = {
                "source": source,
                "destination": destination,
                "days": days,
                "budget": budget,
                "min_hotel_stars": hotel_rating,
                "place_type": None if attraction_type == "None" else attraction_type
            }
            
            # 1. Run the Agentic Logic
            try:
                agent_result = run_travel_agent(travel_params)
                
                # 2. Generate and Display Final Output
                st.success("Trip Planning Complete!")
                
                # Display the formatted itinerary
                itinerary = generate_final_output(agent_result, days)
                st.markdown(itinerary)
                
                # Expandable sections for raw data (optional for transparency)
                with st.expander("View Technical Reasoning/Details"):
                    st.json(agent_result)
                    
            except Exception as e:
                st.error(f"An error occurred during planning: {e}")

else:
    # Initial state message
    st.info("Enter your trip details in the sidebar and click 'Generate Travel Plan' to start.")
