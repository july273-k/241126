import pandas as pd
import plotly.express as px

# Sample data for the periodic table
data = {
    "Element": ["Hydrogen", "Helium", "Lithium", "Beryllium", "Boron", "Carbon", "Nitrogen", "Oxygen", "Fluorine", "Neon"],
    "Symbol": ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne"],
    "Atomic_Number": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Group": [1, 18, 1, 2, 13, 14, 15, 16, 17, 18],
    "Period": [1, 1, 2, 2, 2, 2, 2, 2, 2, 2],
    "Electronegativity": [2.2, None, 0.98, 1.57, 2.04, 2.55, 3.04, 3.44, 3.98, None],
    "State": ["Gas", "Gas", "Solid", "Solid", "Solid", "Solid", "Gas", "Gas", "Gas", "Gas"],
}

# Create DataFrame
df = pd.DataFrame(data)

# Handle missing values by replacing NaN with 0
df["Electronegativity"] = df["Electronegativity"].fillna(0)

# Create interactive periodic table visualization
fig = px.scatter(
    df,
    x="Group",
    y="Period",
    size="Electronegativity",
    color="State",
    text="Symbol",
    title="Creative Periodic Table Example",
    hover_data=["Element", "Atomic_Number", "Electronegativity"],
    labels={"Group": "Group (Column)", "Period": "Period (Row)"},
    size_max=60
)

# Adjust layout
fig.update_traces(textposition="top center")
fig.update_layout(
    xaxis=dict(title="Group", tickmode="linear", dtick=1),
    yaxis=dict(title="Period", tickmode="linear", dtick=1, autorange="reversed"),
    height=600
)

# Show the figure
fig.show()
