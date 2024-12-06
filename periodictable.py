import streamlit as st
import pandas as pd

# Load the dataset
file_path = 'elementdatavalues.csv'  # Replace with the path to your dataset
element_data = pd.read_csv(file_path)

st.title("Interactive Periodic Table")

# Selectbox for choosing an element
selected_symbol = st.selectbox("Select an element:", element_data["Symbol"].sort_values())

# Extract details of the selected element
selected_element = element_data[element_data["Symbol"] == selected_symbol].iloc[0]

st.markdown(f"""
**Element Details**
- **Name**: {selected_element['Name']}
- **Symbol**: {selected_element['Symbol']}
- **Atomic Number**: {selected_element['Atomic_Number']}
- **Atomic Weight**: {selected_element['Atomic_Weight']}
- **Group**: {int(selected_element['Graph.Group'])}
- **Period**: {int(selected_element['Graph.Period'])}
- **Phase**: {selected_element['Phase']}
- **Density**: {selected_element['Density']} g/cm³
- **Melting Point**: {selected_element['Melting_Point']} K
- **Boiling Point**: {selected_element['Boiling_Point']} K
""")

# Define periodic table grid with placeholder elements
grid_template = [["" for _ in range(18)] for _ in range(7)]

# Fill the grid using dataset
for _, row in element_data.iterrows():
    period = int(row['Graph.Period']) - 1  # Zero-indexed
    group = int(row['Graph.Group']) - 1   # Zero-indexed
    grid_template[period][group] = row['Symbol']

# Display periodic table
table_html = """
<style>
.periodic-table {
    display: grid;
    grid-template-columns: repeat(18, 40px);
    grid-gap: 5px;
    text-align: center;
    font-size: 12px;
}
.element {
    border: 1px solid #aaa;
    padding: 5px;
    border-radius: 5px;
    width: 40px;
    height: 40px;
}
.selected {
    background-color: #ffeb3b;
    font-weight: bold;
}
</style>
<div class="periodic-table">
"""

# Create grid HTML
for row in grid_template:
    for symbol in row:
        css_class = "selected" if symbol == selected_symbol else "element"
        table_html += f'<div class="{css_class}">{symbol}</div>' if symbol else '<div class="element"></div>'
table_html += "</div>"

# Render periodic table
st.markdown(table_html, unsafe_allow_html=True)

st.write("Selected element is highlighted in yellow.")
