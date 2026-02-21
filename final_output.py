def generate_final_output(agent_result: str, days: int, destination: str):
    """
    Formats the final agent output for the Streamlit UI.
    """
    # Create a clean header for the user
    output_str = f"## 🗺️ Your Personalized {days}-Day Itinerary for {destination}\n"
    output_str += "---\n\n"
    
    # Since the agent returns a full detailed string with its tool findings, 
    # we append it directly to the output.
    output_str += agent_result
    
    # Optional: Add a footer
    output_str += "\n\n---\n*Safe travels! This plan was generated using real-time tool data.*"
    
    return output_str

def print_expected_results(final_output: str):
    print("\n--- FINAL TRAVEL PLAN ---")
    print(final_output)
    print("-------------------------")
