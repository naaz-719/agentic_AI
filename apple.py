import streamlit as st
import pandas as pd
import plotly.express as px

from agent.travel_agent import run_travel_agent
from output.final_output import generate_final_output

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Agentic AI Travel Planner",
    page_icon="🌍",
    layout="wide"
)

st.markdown("""
<style>

.stApp{
    background-color:#F8FAFC;
}

.block-container{
    padding-top:1rem;
    max-width:1400px;
}

div[data-testid="metric-container"]{
    background:white;
    border-radius:16px;
    padding:20px;
    border:1px solid #E2E8F0;
    box-shadow:0 2px 10px rgba(0,0,0,0.08);
}

div[data-testid="metric-container"] label{
    color:#64748B !important;
}

div[data-testid="metric-container"] [data-testid="stMetricValue"]{
    color:#0F172A !important;
    font-size:2rem !important;
    font-weight:700 !important;
}

.travel-card{
    background:white;
    padding:20px;
    border-radius:16px;
    border:1px solid #E2E8F0;
    box-shadow:0 2px 10px rgba(0,0,0,0.08);
    margin-bottom:15px;
    color:#0F172A;
}

.itinerary-card{
    background:white;
    padding:15px;
    border-left:5px solid #2563EB;
    border-radius:12px;
    border:1px solid #E2E8F0;
    box-shadow:0 2px 10px rgba(0,0,0,0.08);
    margin-bottom:10px;
    color:#0F172A;
}

.stButton button{
    background:#2563EB;
    color:white;
    border:none;
    border-radius:10px;
    height:3rem;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HERO SECTION
# =====================================================
st.markdown("""
<div style="
background:linear-gradient(135deg,#2563EB,#1D4ED8);
padding:30px;
border-radius:20px;
margin-bottom:20px;
color:white;
">

<h1>🌍 Agentic AI Travel Planner</h1>

<h4>AI-Powered Travel Intelligence Platform</h4>

<p>Flights • Hotels • Weather • Budget • Itinerary</p>

</div>
""", unsafe_allow_html=True)

# =====================================================
# INPUTS
# =====================================================
st.subheader("🧳 Travel Preferences")

col1, col2, col3, col4 = st.columns(4)

with col1:
    source = st.text_input(
        "Departure City",
        "Bangalore"
    )

with col2:
    destination = st.text_input(
        "Destination",
        "Goa"
    )

with col3:
    days = st.selectbox(
        "Trip Duration",
        [3, 4, 5, 6, 7]
    )

with col4:
    budget = st.number_input(
        "Max Hotel Budget",
        min_value=1000,
        max_value=20000,
        value=5000,
        step=500
    )

generate_plan = st.button(
    "🚀 Generate Travel Plan",
    use_container_width=True
)

# =====================================================
# DEFAULT COORDINATES
# =====================================================
latitude = 15.2993
longitude = 74.1240

# =====================================================
# GENERATE PLAN
# =====================================================
if generate_plan:

    with st.spinner("🤖 Planning your trip..."):
        agent_result = run_travel_agent({
            "source": source,
            "destination": destination,
            "days": days,
            "budget": budget,
            "latitude": latitude,
            "longitude": longitude
        })

        final_output = generate_final_output(
            agent_result,
            days
        )

    st.success("✅ Your personalized travel plan is ready!")

    flight = final_output["Flight Option Selected"]
    hotel = final_output["Hotel Recommendation"]
    budget_info = final_output["Budget Breakdown"]

    weather_data = []
    for day_name, info in final_output["Weather Forecast"].items():
        weather_data.append({
            "Day": day_name,
            "Max Temp": info["Max Temp"],
            "Min Temp": info["Min Temp"]
        })

    weather_df = pd.DataFrame(weather_data)

    budget_df = pd.DataFrame({
        "Category": ["Flight", "Hotel", "Local"],
        "Cost": [
            budget_info["Flight Cost"],
            budget_info["Hotel Cost"],
            budget_info["Local Expenses"]
        ]
    })

    # =====================================================
    # KPI CARDS
    # =====================================================
    st.subheader("📊 Trip Overview")

    cost_per_day = round(
        budget_info["Total Estimated Budget"] / days
    )

    k1, k2, k3, k4, k5 = st.columns(5)

    k1.metric("📅 Duration", f"{days} Days")
    k2.metric("✈ Flight", f"₹{budget_info['Flight Cost']}")
    k3.metric("🏨 Hotel", f"₹{budget_info['Hotel Cost']}")
    k4.metric("💰 Total", f"₹{budget_info['Total Estimated Budget']}")
    k5.metric("📊 Cost/Day", f"₹{cost_per_day}")

    st.divider()

    st.subheader("📍 Destination Insights")

    i1, i2, i3, i4 = st.columns(4)

    i1.metric("🌴 Destination", destination)
    i2.metric("📅 Duration", f"{days} Days")
    i3.metric("🏨 Hotel Rating", f"{hotel['Stars']} ⭐")
    i4.metric("💰 Budget", f"₹{budget_info['Total Estimated Budget']}")

    st.divider()

    st.subheader("🧠 Travel Intelligence Score")

    score = 70
    if hotel["Stars"] >= 4:
        score += 10
    if budget_info["Total Estimated Budget"] < 20000:
        score += 10
    if days >= 4:
        score += 10

    st.progress(score / 100)
    st.success(f"Overall Trip Score: {score}/100")

    # =====================================================
    # FLIGHT + HOTEL
    # =====================================================
    left, right = st.columns(2)

    with left:
        st.markdown(f"""
<div class="travel-card">
<h3>✈ Flight Details</h3>
<b>Airline:</b> {flight['Airline']}<br>
<b>Price:</b> ₹{flight['Price']}<br>
<b>Departure:</b> {flight['Departure']}<br>
<b>Arrival:</b> {flight['Arrival']}<br>
<b>Duration:</b> {flight['Duration']} Hours
</div>
""", unsafe_allow_html=True)

    with right:
        st.markdown(f"""
<div class="travel-card">
<h3>🏨 Hotel Recommendation</h3>
<b>Hotel:</b> {hotel['Hotel Name']}<br>
<b>Stars:</b> ⭐ {hotel['Stars']}<br>
<b>Price/Night:</b> ₹{hotel['Price Per Night']}<br>
<b>Amenities:</b> {", ".join(hotel['Amenities'])}
</div>
""", unsafe_allow_html=True)

    st.divider()
    st.subheader("📊 Travel Analytics")

    left_chart, right_chart = st.columns(2)

    with left_chart:
        fig_weather = px.line(
            weather_df,
            x="Day",
            y=["Max Temp", "Min Temp"],
            markers=True,
            title="Temperature Forecast"
        )
        st.plotly_chart(fig_weather, use_container_width=True)

    with right_chart:
        fig_budget = px.pie(
            budget_df,
            values="Cost",
            names="Category",
            hole=0.5,
            title="Budget Allocation"
        )
        st.plotly_chart(fig_budget, use_container_width=True)

    st.divider()

    # =====================================================
    # WEATHER
    # =====================================================
    st.subheader("🌦 Weather Forecast")

    for day_name, info in final_output["Weather Forecast"].items():
        st.info(
            f"""
📅 {day_name}
🌡 Max Temp : {info['Max Temp']}°C
🌡 Min Temp : {info['Min Temp']}°C
💨 Wind Speed : {info['Wind Speed']} km/h
"""
        )

    # =====================================================
    # ITINERARY
    # =====================================================
    st.subheader("🗺 Travel Itinerary")

    for day_name, details in final_output["Day-wise Itinerary"].items():
        st.markdown(f"""
<div class="itinerary-card">
<h4>{day_name}</h4>
{details['Activity']}
</div>
""", unsafe_allow_html=True)

    st.divider()

    # =====================================================
    # BUDGET
    # =====================================================
    st.subheader("💰 Budget Breakdown")

    b1, b2, b3 = st.columns(3)

    b1.metric("✈ Flight", f"₹{budget_info['Flight Cost']}")
    b2.metric("🏨 Hotel", f"₹{budget_info['Hotel Cost']}")
    b3.metric("🍽 Local", f"₹{budget_info['Local Expenses']}")

    st.metric(
        "💵 Total Estimated Cost",
        f"₹{budget_info['Total Estimated Budget']}"
    )

    # =====================================================
    # AI RECOMMENDATION
    # =====================================================
    st.divider()

    st.subheader("🤖 AI Recommendation")

    st.success(
        f"""
This {days}-day trip to {destination} 
offers a balanced combination of 
budget, accommodation quality, 
weather conditions and local attractions.

Recommended for leisure travelers 
seeking a value-for-money experience.
"""
    )

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.caption(
    "Built using Streamlit, LangChain, Plotly and Agentic AI workflows."
)
