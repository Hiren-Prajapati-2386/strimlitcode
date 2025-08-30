import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Battery Cell Data", page_icon="🔋", layout="wide")

st.title("🔋 Battery Cell Data Entry")
st.write("Enter your cell details and calculate their capacity.")

# Step 1: Enter cell types
st.subheader("Step 1: Enter Cell Types")
num_cells = st.number_input("How many cells do you want to enter?", min_value=1, max_value=20, value=8)

cell_types = []

with st.form("cell_form"):
    for i in range(num_cells):
        cell_type = st.text_input(f"Cell type #{i+1} (e.g., lfp/nmc)", key=f"cell_{i}").strip().lower()
        cell_types.append(cell_type)
    submitted = st.form_submit_button("Save Cell Types")

cells_data = {}
if submitted:
    for idx, cell_type in enumerate(cell_types, start=1):
        if not cell_type:
            continue
        cell_key = f"cell_{idx}_{cell_type}"

        voltage = 3.2 if cell_type == "lfp" else 3.6
        min_voltage = 2.8 if cell_type == "lfp" else 3.2
        max_voltage = 3.6 if cell_type == "lfp" else 4.0
        current = 0.0
        temp = round(random.uniform(25, 40), 1)
        capacity = round(voltage * current, 2)

        cells_data[cell_key] = {
            "voltage": voltage,
            "current": current,
            "temp": temp,
            "capacity": capacity,
            "min_voltage": min_voltage,
            "max_voltage": max_voltage
        }

    st.success("✅ Cell types saved successfully!")

# Step 2: Enter current for each cell
if cells_data:
    st.subheader("Step 2: Enter Current for Each Cell")
    for key in cells_data:
        current = st.number_input(f"Current for {key} (A)", min_value=0.0, step=0.1, key=f"current_{key}")
        voltage = cells_data[key]["voltage"]
        cells_data[key]["current"] = current
        cells_data[key]["capacity"] = round(voltage * current, 2)

    # Convert to DataFrame for display
    df = pd.DataFrame.from_dict(cells_data, orient="index")

    st.subheader("📊 Updated Cell Data")
    st.dataframe(df.style.highlight_max(axis=0, color="lightgreen"))

    # Option to download data
    csv = df.to_csv().encode("utf-8")
    st.download_button(
        label="⬇️ Download Data as CSV",
        data=csv,
        file_name="cell_data.csv",
        mime="text/csv",
    )
