from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, Tool
import core
import json
import os

llm = ChatGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
    model="llama-3.3-70b-specdec"
)


def tool_plan(query):
    q = json.loads(query)
    return core.plan_trip(q["source"], q["destination"], q["days"])


def tool_flights(query):
    q = json.loads(query)
    return core.search_flights(q["source"], q["destination"])


tools = [
    Tool(
        name="trip_planner",
        func=tool_plan,
        description="Plan a full trip"
    ),
    Tool(
        name="search_flights",
        func=tool_flights,
        description="Search flights"
    ),
]

agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True,
)

def ask_agent(source, destination, days):
    query = f"Plan a {days} day trip from {source} to {destination}"
    return agent.run(query)
