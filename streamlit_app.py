import streamlit as st
import core
import agent

st.set_page_config(page_title="Agentic AI Travel Planner")

st.title("🧭 Agentic AI Travel Planner")

source = st.text_input("Source city")
destination = st.text_input("Destination city")
days = st.number_input("Trip duration (days)", min_value=1, max_value=10, value=3)

preferences = st.multiselect(
    "Choose your interests",
    ["Beaches", "Temples", "Shopping", "Nature", "Adventure"]
)

if st.button("Generate Trip"):
    trip = core.plan_trip(source, destination, int(days))

    if "error" in trip:
        st.error(trip["error"])
    else:
        st.success("Trip generated successfully")

        st.subheader("✈ Flight")
        st.write(trip["flight_selected"])

        st.subheader("🏨 Hotel")
        st.write(trip["hotel_selected"])

        st.subheader("🗺 Itinerary")
        st.write(trip["itinerary"])

        st.subheader("💰 Budget")
        st.write(trip["budget"])

        # agentic LLM reasoning summary
        st.subheader("🧠 AI Travel Agent Summary")
        summary = agent.ask_agent(
            f"Plan a {days}-day trip from {source} to {destination} including {', '.join(preferences)}"
        )
        st.write(summary)

        # PDF download
        if st.button("📥 Download PDF"):
            path = "/tmp/trip_plan.pdf"
            core.generate_pdf(trip, path)
            with open(path, "rb") as f:
                st.download_button("Download Trip Plan", f, file_name="trip_plan.pdf")


