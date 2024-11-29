pip install streamlit pandas matplotlib
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize game state
if "year" not in st.session_state:
    st.session_state.year = 1
    st.session_state.environment_score = 50
    st.session_state.economy_score = 50
    st.session_state.society_score = 50
    st.session_state.history = []

# Constants
MAX_YEARS = 20
POLICIES = {
    "Invest in renewable energy": {"cost": -5, "environment": 10, "economy": 2, "society": 3},
    "Subsidize public transport": {"cost": -3, "environment": 7, "economy": -1, "society": 5},
    "Increase carbon tax": {"cost": -4, "environment": 15, "economy": -5, "society": -2},
    "Promote electric vehicles": {"cost": -6, "environment": 8, "economy": 1, "society": 4},
    "Expand industrial production": {"cost": -10, "environment": -8, "economy": 10, "society": -5},
}

# Helper functions
def apply_policy(policy):
    """Apply the effects of a selected policy."""
    effects = POLICIES[policy]
    st.session_state.environment_score += effects["environment"]
    st.session_state.economy_score += effects["economy"]
    st.session_state.society_score += effects["society"]
    st.session_state.history.append({
        "Year": st.session_state.year,
        "Policy": policy,
        "Environment": st.session_state.environment_score,
        "Economy": st.session_state.economy_score,
        "Society": st.session_state.society_score
    })

def reset_game():
    """Reset the game state."""
    st.session_state.year = 1
    st.session_state.environment_score = 50
    st.session_state.economy_score = 50
    st.session_state.society_score = 50
    st.session_state.history = []

# UI layout
st.title("Climate Change Game")
st.header(f"Year {st.session_state.year}")

if st.session_state.year > MAX_YEARS:
    st.success("Game Over! Here's how you managed your country:")
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df)

    # Plot results
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(history_df["Year"], history_df["Environment"], label="Environment Score", color="green")
    ax.plot(history_df["Year"], history_df["Economy"], label="Economy Score", color="blue")
    ax.plot(history_df["Year"], history_df["Society"], label="Society Score", color="orange")
    ax.set_xlabel("Year")
    ax.set_ylabel("Score")
    ax.legend()
    st.pyplot(fig)

    if st.button("Restart Game"):
        reset_game()
else:
    st.subheader("Current Scores")
    st.metric("Environment Score", st.session_state.environment_score)
    st.metric("Economy Score", st.session_state.economy_score)
    st.metric("Society Score", st.session_state.society_score)

    st.subheader("Choose a Policy for This Year")
    policy = st.radio("Select a policy:", list(POLICIES.keys()))

    if st.button("Apply Policy"):
        apply_policy(policy)
        st.session_state.year += 1
        st.experimental_rerun()
