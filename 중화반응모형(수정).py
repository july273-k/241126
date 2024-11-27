import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
import pandas as pd
import time

# Create star shape
def create_star(center, size):
    """
    Creates a star shape as a Polygon object.
    :param center: Tuple of (x, y) for the center of the star.
    :param size: Size of the star (radius of the outer points).
    :return: Polygon object representing the star.
    """
    x, y = center
    outer_radius = size
    inner_radius = size * 0.5  # Inner radius of the star

    # Define angles for outer and inner points of the star
    angles = np.linspace(0, 2 * np.pi, 10, endpoint=False)
    points = []
    for i, angle in enumerate(angles):
        radius = outer_radius if i % 2 == 0 else inner_radius
        points.append((x + radius * np.cos(angle), y + radius * np.sin(angle)))

    # Create a polygon for the star shape
    return Polygon(points, closed=True, color='yellow', alpha=0.7)

# Plot the particles with star effects
def plot_particles(acid_positions, base_positions, water_positions, reaction_effects):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Plot particles
    ax.scatter(acid_positions[:, 0], acid_positions[:, 1], color='red', label="H⁺ (Acid)", s=50)
    ax.scatter(base_positions[:, 0], base_positions[:, 1], color='blue', label="OH⁻ (Base)", s=50)
    ax.scatter(water_positions[:, 0], water_positions[:, 1], color='green', label="H₂O (Water)", s=50)

    # Plot reaction effects as stars
    for effect in reaction_effects:
        star = create_star((effect[0], effect[1]), effect[2] * 0.5)  # Reduced size
        ax.add_patch(star)

    ax.legend()
    ax.set_title("Neutralization Reaction Simulation with Star Effects")
    ax.axis("off")
    return fig

# Example update_particles function to generate reaction effects
def update_particles(acid_positions, base_positions, water_positions, reaction_effects):
    reacted_pairs = 0
    new_water_positions = []
    new_effect_positions = []

    # Check for collisions (simplified proximity check)
    i = 0
    while i < len(acid_positions):
        j = 0
        while j < len(base_positions):
            if np.linalg.norm(acid_positions[i] - base_positions[j]) < 0.05:  # Collision threshold
                new_water_positions.append((acid_positions[i] + base_positions[j]) / 2)
                new_effect_positions.append([acid_positions[i, 0], acid_positions[i, 1], 0.05])  # Initial star size
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
        reaction_effects[:, 2] += 0.005  # Increase size gradually
        reaction_effects = reaction_effects[reaction_effects[:, 2] < 0.15]  # Remove large effects

    # Random motion for remaining particles
    acid_positions += np.random.uniform(-0.03, 0.03, acid_positions.shape)
    base_positions += np.random.uniform(-0.03, 0.03, base_positions.shape)
    water_positions += np.random.uniform(-0.015, 0.015, water_positions.shape)

    # Keep particles within bounds
    acid_positions = np.clip(acid_positions, 0, 1)
    base_positions = np.clip(base_positions, 0, 1)
    water_positions = np.clip(water_positions, 0, 1)

    return acid_positions, base_positions, water_positions, reacted_pairs, reaction_effects

# Streamlit App
st.title("Neutralization Reaction Simulation with Star Effects")

st.sidebar.header("Particle Settings")
acid_count = st.sidebar.slider("Number of Acid Particles (H⁺)", 0, 50, 25, 1)
base_count = st.sidebar.slider("Number of Base Particles (OH⁻)", 0, 50, 25, 1)

if st.button("Start Reaction"):
    with st.spinner("Running simulation..."):
        # Initialize particles
        acid_positions = np.random.rand(acid_count, 2)
        base_positions = np.random.rand(base_count, 2)
        water_positions = np.empty((0, 2))
        reaction_effects = np.empty((0, 3))  # [x, y, size]

        total_reacted_pairs = 0
        animation_placeholder = st.empty()
        table_placeholder = st.empty()

        # Run the simulation
        while len(acid_positions) > 0 and len(base_positions) > 0:
            acid_positions, base_positions, water_positions, reacted_pairs, reaction_effects = update_particles(
                acid_positions, base_positions, water_positions, reaction_effects
            )
            total_reacted_pairs += reacted_pairs
            fig = plot_particles(acid_positions, base_positions, water_positions, reaction_effects)

            # Update visualization
            animation_placeholder.pyplot(fig)
            time.sleep(0.05)  # Update every 50ms

        st.success("Reaction completed!")
