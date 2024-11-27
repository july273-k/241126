import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

# Initialize particles
def initialize_particles(acid_count, base_count):
    acid_positions = np.random.rand(acid_count, 2)  # Random positions for acid
    base_positions = np.random.rand(base_count, 2)  # Random positions for base
    water_positions = np.empty((0, 2))  # Initially no water molecules
    reaction_effects = np.empty((0, 3))  # [x, y, size] for reaction effects
    return acid_positions, base_positions, water_positions, reaction_effects

# Update particle positions and simulate reaction with attraction
def update_particles(acid_positions, base_positions, water_positions, reaction_effects, attraction_strength=0.01):
    reacted_pairs = 0
    new_water_positions = []
    new_effect_positions = []

    # Apply attraction force between H⁺ and OH⁻
    for acid in acid_positions:
        for base in base_positions:
            direction = base - acid
            distance = np.linalg.norm(direction)
            if distance > 0:  # Avoid division by zero
                attraction_force = attraction_strength * direction / distance
                acid += attraction_force
                base -= attraction_force

    # Check for collisions and react
    i = 0
    while i < len(acid_positions):
        j = 0
        while j < len(base_positions):
            if np.linalg.norm(acid_positions[i] - base_positions[j]) < 0.05:  # Collision threshold
                new_water_positions.append((acid_positions[i] + base_positions[j]) / 2)
                new_effect_positions.append([acid_positions[i, 0], acid_positions[i, 1], 0.05])  # Initial effect size
                acid_positions = np.delete(acid_positions, i, axis=0)
                base_positions = np.delete(base_positions, j, axis=0)
                reacted_pairs += 1
                break
            else:
                j += 1
        else:
            i += 1

    # Add water positions if any reactions occurred
    if new_water_positions:
        new_water_positions = np.array(new_water_positions)
        water_positions = np.vstack([water_positions, new_water_positions])

    # Add new reaction effects
    if new_effect_positions:
        new_effect_positions = np.array(new_effect_positions)
        reaction_effects = np.vstack([reaction_effects, new_effect_positions])

    # Update existing reaction effects (increase size and fade out)
    if len(reaction_effects) > 0:
        reaction_effects[:, 2] += 0.005  # Increase effect size
        reaction_effects = reaction_effects[reaction_effects[:, 2] < 0.15]  # Remove effects that are too large

    # Random motion for remaining particles
    acid_positions += np.random.uniform(-0.03, 0.03, acid_positions.shape)
    base_positions += np.random.uniform(-0.03, 0.03, base_positions.shape)
    water_positions += np.random.uniform(-0.015, 0.015, water_positions.shape)

    # Keep particles within bounds
    acid_positions = np.clip(acid_positions, 0, 1)
    base_positions = np.clip(base_positions, 0, 1)
    water_positions = np.clip(water_positions, 0, 1)

    return acid_positions, base_positions, water_positions, reacted_pairs, reaction_effects

# Plot the particles
def plot_particles(acid_positions, base_positions, water_positions, reaction_effects):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Plot particles
    ax.scatter(acid_positions[:, 0], acid_positions[:, 1], color='red', label="H⁺ (Acid)", s=50)
    ax.scatter(base_positions[:, 0], base_positions[:, 1], color='blue', label="OH⁻ (Base)", s=50)
    ax.scatter(water_positions[:, 0], water_positions[:, 1], color='yellow', label="H₂O (Water)", s=50)

    # Plot reaction effects
    for effect in reaction_effects:
        circle = plt.Circle((effect[0], effect[1]), effect[2], color='green', alpha=0.5)
        ax.add_patch(circle)

    ax.legend()
    ax.set_title("Neutralization Reaction Simulation with Attraction")
    ax.axis("off")
    return fig

# Streamlit App
st.title("중화 반응 모형")

st.sidebar.header("초기 반응 조건")
acid_count = st.sidebar.slider("Number of Acid Particles (H⁺)", 1, 50, 10, 1)
base_count = st.sidebar.slider("Number of Base Particles (OH⁻)", 1, 50, 10, 1)
attraction_strength = st.sidebar.slider("Attraction Strength", 0.001, 0.05, 0.01, 0.001)

if st.button("반응 시작작"):
    with st.spinner("Running simulation..."):
        # Initialize particles
        acid_positions, base_positions, water_positions, reaction_effects = initialize_particles(acid_count, base_count)

        total_reacted_pairs = 0
        animation_placeholder = st.empty()
        table_placeholder = st.empty()

        # Run the animation
        while len(acid_positions) > 0 and len(base_positions) > 0:  # Stop when all particles have reacted
            acid_positions, base_positions, water_positions, reacted_pairs, reaction_effects = update_particles(
                acid_positions, base_positions, water_positions, reaction_effects, attraction_strength
            )
            total_reacted_pairs += reacted_pairs
            fig = plot_particles(acid_positions, base_positions, water_positions, reaction_effects)

            # Update table
            reacted_acid_count = -(acid_count - len(acid_positions))  # Negative for reacted acids
            reacted_base_count = -(base_count - len(base_positions))  # Negative for reacted bases
            created_water_count = f"+{len(water_positions)}"  # Positive with + for water molecules

            results = {
                "Particle Type": ["H⁺ (Acid)", "OH⁻ (Base)", "H₂O (Water)"],
                "Initial Count": [acid_count, base_count, 0],
                "Reacted (Generated)": [reacted_acid_count, reacted_base_count, created_water_count],
                "Remaining": [len(acid_positions), len(base_positions), len(water_positions)],
            }
            table_placeholder.table(pd.DataFrame(results))

            animation_placeholder.pyplot(fig)
            time.sleep(0.01)  # 1/100 second update time

        st.success("반응이 완료됐습니다!")

