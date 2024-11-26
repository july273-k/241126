import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

# Initialize particles
def initialize_particles(acid_moles, base_moles):
    acid_positions = np.random.rand(int(acid_moles * 10), 2)
    base_positions = np.random.rand(int(base_moles * 10), 2)
    water_positions = np.empty((0, 2))  # Initially no water molecules
    return acid_positions, base_positions, water_positions

# Update particle positions and simulate reaction
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
                new_effect_positions.append((acid_positions[i] + base_positions[j]) / 2)  # Effect position
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
        new_water_positions = np.array(new_water_positions)  # Convert list to array
        water_positions = np.vstack([water_positions, new_water_positions])

    # Add reaction effects
    if new_effect_positions:
        new_effect_positions = np.array(new_effect_positions)
        reaction_effects = np.vstack([reaction_effects, new_effect_positions])

    # Random motion for remaining particles
    acid_positions += np.random.uniform(-0.03, 0.03, acid_positions.shape)  # Increased speed by 50%
    base_positions += np.random.uniform(-0.03, 0.03, base_positions.shape)
    water_positions += np.random.uniform(-0.015, 0.015, water_positions.shape)

    # Keep particles within bounds
    acid_positions = np.clip(acid_positions, 0, 1)
    base_positions = np.clip(base_positions, 0, 1)
    water_positions = np.clip(water_positions, 0, 1)

    return acid_positions, base_positions, water_positions, reacted_pairs, reaction_effects

# Plot the particles
def plot_particles(acid_positions, base_positions, water_positions, reaction_effects, step):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.scatter(acid_positions[:, 0], acid_positions[:, 1], color='red', label="H⁺ (acid)", s=50)  # Red for H⁺
    ax.scatter(base_positions[:, 0], base_positions[:, 1], color='blue', label="OH⁻ (base)", s=50)  # Blue for OH⁻
    ax.scatter(water_positions[:, 0], water_positions[:, 1], color='yellow', label="H₂O (water)", s=50)  # Yellow for water

    # Add reaction effect (pulse effect)
    for effect in reaction_effects:
        circle = plt.Circle(effect, 0.03 * (1 + 0.1 * (step % 5)), color='green', alpha=0.5)
        ax.add_patch(circle)

    ax.legend()
    ax.set_title("Dynamic Neutralization Reaction")
    ax.axis("off")
    return fig

# Streamlit App
st.title("중화 반응 시뮬레이션")

st.sidebar.header("반응 조건")

acid_concentration = st.sidebar.slider("산 농도 (mol/L)", 0.1, 2.0, 1.0, 0.1)
base_concentration = st.sidebar.slider("염기 농도 (mol/L)", 0.1, 2.0, 1.0, 0.1)
acid_volume_ml = st.sidebar.slider("산 용액 부피 (mL)", 0, 2000, 1000, 10)  # Minimum 0mL, step 10mL
base_volume_ml = st.sidebar.slider("염기 용액 부피 (mL)", 0, 2000, 1000, 10)  # Minimum 0mL, step 10mL

if st.button("반응 시뮬레이션 시작"):
    with st.spinner("시뮬레이션 실행 중..."):
        # Convert mL to L for calculations
        acid_volume = acid_volume_ml / 1000.0
        base_volume = base_volume_ml / 1000.0

        # Calculate initial moles
        acid_moles = acid_concentration * acid_volume
        base_moles = base_concentration * base_volume

        # Initialize particles
        acid_positions, base_positions, water_positions = initialize_particles(acid_moles, base_moles)
        reaction_effects = np.empty((0, 2))  # Track effect positions

        total_reacted_pairs = 0  # Track total reactions
        animation_placeholder = st.empty()
        table_placeholder = st.empty()

        # Run the animation
        step = 0
        initial_acid_ions = int(acid_moles * 10)
        initial_base_ions = int(base_moles * 10)

        while len(acid_positions) > 0 and len(base_positions) > 0:  # Continue until all reactions complete
            acid_positions, base_positions, water_positions, reacted_pairs, reaction_effects = update_particles(
                acid_positions, base_positions, water_positions, reaction_effects
            )
            total_reacted_pairs += reacted_pairs
            fig = plot_particles(acid_positions, base_positions, water_positions, reaction_effects, step)

            # Remove effects after 3 seconds
            if step > 30:
                reaction_effects = reaction_effects[1:]  # Remove oldest effect

            # Real-time table update
            reacted_acid_ions = initial_acid_ions - len(acid_positions)
            reacted_base_ions = initial_base_ions - len(base_positions)
            total_water_molecules = len(water_positions)

            results = {
                "이온 종류": ["H⁺ (산)", "OH⁻ (염기)", "H₂O (물)"],
                "초기 개수": [initial_acid_ions, initial_base_ions, 0],
                "반응한 개수": [reacted_acid_ions, reacted_base_ions, total_water_molecules],
                "남은 개수": [len(acid_positions), len(base_positions), total_water_molecules],
            }
            table_placeholder.table(pd.DataFrame(results))

            animation_placeholder.pyplot(fig)
            step += 1
            time.sleep(0.001)  # 1/1000 second update time

        st.success("시뮬레이션 완료!")