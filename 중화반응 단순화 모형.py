import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Initialize particles
def initialize_particles(acid_count, base_count):
    acid_positions = np.random.rand(acid_count, 2)
    base_positions = np.random.rand(base_count, 2)
    water_positions = []
    reaction_effects = []
    return acid_positions, base_positions, water_positions, reaction_effects

# Efficient update with vectorized operations
def update_particles(acid_positions, base_positions, water_positions, reaction_effects):
    if len(acid_positions) == 0 or len(base_positions) == 0:
        return acid_positions, base_positions, water_positions, 0, reaction_effects

    # Compute pairwise distances
    acid_expanded = acid_positions[:, np.newaxis, :]
    base_expanded = base_positions[np.newaxis, :, :]
    distances = np.linalg.norm(acid_expanded - base_expanded, axis=2)

    # Find collisions
    collision_indices = np.argwhere(distances < 0.05)

    # Process reactions
    reacted_pairs = 0
    for acid_idx, base_idx in collision_indices:
        if acid_idx < len(acid_positions) and base_idx < len(base_positions):
            reacted_pairs += 1
            water_positions.append((acid_positions[acid_idx] + base_positions[base_idx]) / 2)
            reaction_effects.append([*acid_positions[acid_idx], 0.05])  # Add effect
            acid_positions = np.delete(acid_positions, acid_idx, axis=0)
            base_positions = np.delete(base_positions, base_idx, axis=0)
            break  # Avoid index mismatch due to deletion

    # Update reaction effects
    reaction_effects = [[x, y, size + 0.005] for x, y, size in reaction_effects if size < 0.15]

    # Random motion
    acid_positions += np.random.uniform(-0.03, 0.03, acid_positions.shape)
    base_positions += np.random.uniform(-0.03, 0.03, base_positions.shape)
    water_positions = np.array(water_positions) + np.random.uniform(-0.015, 0.015, (len(water_positions), 2))

    # Keep within bounds
    acid_positions = np.clip(acid_positions, 0, 1)
    base_positions = np.clip(base_positions, 0, 1)
    if len(water_positions) > 0:
        water_positions = np.clip(water_positions, 0, 1)

    return acid_positions, base_positions, water_positions, reacted_pairs, reaction_effects

# Efficient plotting
def plot_particles(fig, ax, acid_positions, base_positions, water_positions, reaction_effects):
    ax.clear()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Plot particles
    ax.scatter(acid_positions[:, 0], acid_positions[:, 1], color='red', label="H⁺ (Acid)", s=50)
    ax.scatter(base_positions[:, 0], base_positions[:, 1], color='blue', label="OH⁻ (Base)", s=50)
    if len(water_positions) > 0:
        ax.scatter(water_positions[:, 0], water_positions[:, 1], color='yellow', label="H₂O (Water)", s=50)

    # Plot reaction effects
    for x, y, size in reaction_effects:
        circle = plt.Circle((x, y), size, color='green', alpha=0.5)
        ax.add_patch(circle)

    ax.legend()
    ax.set_title("Efficient Neutralization Reaction Simulation")
    ax.axis("off")

# Streamlit app
st.title("효율적인 중화 반응 시뮬레이션")

acid_count = st.sidebar.slider("산 입자 수 (H⁺)", 0, 50, 25, 1)
base_count = st.sidebar.slider("염기 입자 수 (OH⁻)", 0, 50, 25, 1)

if st.button("반응 시작"):
    acid_positions, base_positions, water_positions, reaction_effects = initialize_particles(acid_count, base_count)

    fig, ax = plt.subplots(figsize=(6, 6))
    animation_placeholder = st.empty()

    while len(acid_positions) > 0 and len(base_positions) > 0:
        acid_positions, base_positions, water_positions, _, reaction_effects = update_particles(
            acid_positions, base_positions, water_positions, reaction_effects
        )
        plot_particles(fig, ax, acid_positions, base_positions, np.array(water_positions), reaction_effects)
        animation_placeholder.pyplot(fig, clear_figure=False)
