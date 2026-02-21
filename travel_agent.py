import os
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType

# Import your real tools from their respective files
from hotel_tool import hotel_recommendation_tool
from place_tool import places_discovery_tool
from weather_tool import weather_lookup_tool
from budget_tool import budget_estimation_tool

def run_travel_agent(travel_params: dict):
    """
    Orchestrates the agentic reasoning loop using LangChain.
    The agent will decide which tools to call based on the user's input.
    """
    # 1. Initialize the LLM (The "Brain")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    # 2. List the "Arms" (Tools) the agent can use
    tools = [
        hotel_recommendation_tool,
        places_discovery_tool,
        weather_lookup_tool,
        budget_estimation_tool
    ]
    
    # 3. Initialize the Agent with a Reasoning Loop (ReAct)
    agent = initialize_agent(
        tools, 
        llm, 
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True  # This allows you to see the "Thinking" process in your console
    )

    # 4. Construct a prompt that forces the agent to use all tools
    query = (
        f"Create a travel plan for a {travel_params['days']}-day trip to {travel_params['destination']} "
        f"from {travel_params['source']} with a total budget of {travel_params['budget']} INR. "
        f"Use your tools to find 3-star hotels, top attractions, and check the weather "
        f"for {travel_params['destination']} (Lat: 28.6, Lon: 77.2)."
    )
    
    # 5. Execute and return the generated itinerary
    return agent.run(query)
