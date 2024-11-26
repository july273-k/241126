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
    return acid_positions, base_positions, water_positions

# Update particle positions and simulate reaction
def update_particles(acid_positions, base_positions, water_positions):
    reacted_pairs = 0
    new_water_positions = []

    # Check for collisions
    i = 0
    while i < len(acid_positions):
        j = 0
        while j < len(base_positions):
            if np.linalg.norm(acid_positions[i] - base_positions[j]) < 0.05:  # Collision threshold
                new_water_positions.append((acid_positions[i] + base_positions[j]) / 2)
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

    # Random motion for remaining particles
    acid_positions += np.random.uniform(-0.03, 0.03, acid_positions.shape)
    base_positions += np.random.uniform(-0.03, 0.03, base_positions.shape)
    water_positions += np.random.uniform(-0.015, 0.015, water_positions.shape)

    # Keep particles within bounds
    acid_positions = np.clip(acid_positions, 0, 1)
    base_positions = np.clip(base_positions, 0, 1)
    water_positions = np.clip(water_positions, 0, 1)

    return acid_positions, base_positions, water_positions, reacted_pairs

# Plot the particles
def plot_particles(acid_positions, base_positions, water_positions):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.scatter(acid_positions[:, 0], acid_positions[:, 1], color='red', label="H⁺ (Acid)", s=50)  # Red for H⁺
    ax.scatter(base_positions[:, 0], base_positions[:, 1], color='blue', label="OH⁻ (Base)", s=50)  # Blue for OH⁻
    ax.scatter(water_positions[:, 0], water_positions[:, 1], color='yellow', label="H₂O (Water)", s=50)  # Yellow for water

    ax.legend()
    ax.set_title("Simple Neutralization Reaction Simulation")  # Title in English
    ax.axis("off")
    return fig

# Streamlit App
st.title("간단한 중화 반응 시뮬레이션")

st.sidebar.header("입자 설정")
acid_count = st.sidebar.slider("산 입자 수 (H⁺)", 1, 100, 50, 1)
base_count = st.sidebar.slider("염기 입자 수 (OH⁻)", 1, 100, 50, 1)

if st.button("반응 시작"):
    with st.spinner("반응 시뮬레이션 실행 중..."):
        # Initialize particles
        acid_positions, base_positions, water_positions = initialize_particles(acid_count, base_count)

        total_reacted_pairs = 0
        animation_placeholder = st.empty()
        table_placeholder = st.empty()

        # Run the animation
        while len(acid_positions) > 0 and len(base_positions) > 0:  # Stop when all particles have reacted
            acid_positions, base_positions, water_positions, reacted_pairs = update_particles(
                acid_positions, base_positions, water_positions
            )
            total_reacted_pairs += reacted_pairs
            fig = plot_particles(acid_positions, base_positions, water_positions)

            # Update table
            results = {
                "입자 종류": ["H⁺ (산)", "OH⁻ (염기)", "H₂O (물)"],
                "초기 개수": [acid_count, base_count, 0],
                "반응한 개수": [acid_count - len(acid_positions), base_count - len(base_positions), len(water_positions)],
                "남은 개수": [len(acid_positions), len(base_positions), len(water_positions)],
            }
            table_placeholder.table(pd.DataFrame(results))

            animation_placeholder.pyplot(fig)
            time.sleep(0.1)

        st.success("모든 반응이 완료되었습니다!")
