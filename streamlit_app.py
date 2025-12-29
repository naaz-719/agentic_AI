import streamlit as st
import core
import agent
import os

st.set_page_config(page_title="Agentic AI Travel Planner")

st.title("🧭 Agentic AI Travel Planner")


source = st.text_input("Source City")
destination = st.text_input("Destination City")
days = st.number_input("Trip Duration", 1, 10, 3)

preference = st.selectbox(
    "Choose interest",
    ["None","beaches","temples","shopping","nature","adventure"]
)

if st.button("Generate Plan"):

    trip = core.plan_trip(source, destination, days)

    st.success("Trip Generated")

    st.subheader("Itinerary")
    st.write(trip["itinerary"])

    st.subheader("Budget")
    st.write(trip["budget"])

    if st.button("🔊 Speak Budget"):
        core.speak_budget(trip["budget"])

    if st.button("📥 Download PDF"):
        path = "trip_plan.pdf"
        core.generate_pdf(trip, path)
        with open(path, "rb") as f:
            st.download_button("Download", f, "trip_plan.pdf")
