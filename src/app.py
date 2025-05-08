import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os
from typing import Dict, List, Tuple

from marine_calculator import calculate_shear_force_and_bending_moment
from data_processor import calculateResults
from visualizer import (
    plot_shear_force_by_section,
    plot_shear_force_by_time,
    plot_bending_moment_by_section,
    plot_bending_moment_by_time,
)

# Configure page
st.set_page_config(
    page_title="Marine System Analysis",
    page_icon="🌊",
    layout="wide"
)

# Title and description
st.title("Marine System Analysis")
st.markdown("""
This application analyzes marine systems by calculating shear forces and bending moments.
Upload your input file and adjust the parameters to see the results.
""")

# Sidebar for input parameters
st.sidebar.header("Ship Parameters")
lamdaByL = st.sidebar.number_input("λ / L:", value=1.2, step=0.01)
length = st.sidebar.number_input("Length (m):", value=134.0, step=0.1)
draft = st.sidebar.number_input("Draft (m):", value=6.7, step=0.1)
displacement = st.sidebar.number_input("Displacement (tons):", value=14000, step=100)
bml = st.sidebar.number_input("BML (m):", value=5.0, step=0.1)

# Main content area
st.header("Input Data")
uploaded_file = st.file_uploader("Upload a .txt input file", type=["txt"])

if uploaded_file:
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", "in.txt")
    
    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File saved to: {file_path}")

    # Time settings
    st.header("Time Settings")
    col1, col2, col3 = st.columns(3)
    with col1:
        t_min = st.number_input("Start time t_min (s):", value=0)
    with col2:
        t_max = st.number_input("End time t_max (s):", value=10)
    with col3:
        num_points = st.number_input("Number of time points:", value=100, min_value=10)

    # Generate time array
    t = np.linspace(t_min, t_max, num_points)

    try:
        # Calculate output parameters
        output_data = calculateResults(lamdaByL, length, draft, displacement, bml)
        
        if not output_data:
            st.error("Failed to calculate results. Please check your input data.")
        else:
            # Perform shear force and bending moment calculation
            shear_force, bending_moment = calculate_shear_force_and_bending_moment(
                output_data['a33'], output_data['b33'], output_data['c33'],
                output_data['a55'], output_data['b55'], output_data['c55'],
                output_data['omega'], output_data['Awl'], displacement,
                output_data['I55'], bml, output_data['section_positions'], t
            )

            # Display results
            st.header("Results")
            
            # Shear Force Plots
            st.subheader("Shear Force Analysis")
            col1, col2 = st.columns(2)
            
            with col1:
                x_val_shear = st.slider(
                    "Select section position for shear force (m):",
                    min_value=float(output_data['section_positions'][0]),
                    max_value=float(output_data['section_positions'][-1]),
                    value=float(output_data['section_positions'][0])
                )
                fig, ax = plt.subplots()
                plot_shear_force_by_section(x_val_shear, output_data['section_positions'], shear_force, t, ax)
                st.pyplot(fig)
            
            with col2:
                t_val_shear = st.slider(
                    "Select time for shear force (s):",
                    min_value=float(t[0]),
                    max_value=float(t[-1]),
                    value=float(t[0])
                )
                fig, ax = plt.subplots()
                plot_shear_force_by_time(t_val_shear, t, output_data['section_positions'], shear_force, ax)
                st.pyplot(fig)

            # Bending Moment Plots
            st.subheader("Bending Moment Analysis")
            col1, col2 = st.columns(2)
            
            with col1:
                x_val_bending = st.slider(
                    "Select section position for bending moment (m):",
                    min_value=float(output_data['section_positions'][0]),
                    max_value=float(output_data['section_positions'][-1]),
                    value=float(output_data['section_positions'][0])
                )
                fig, ax = plt.subplots()
                plot_bending_moment_by_section(x_val_bending, output_data['section_positions'], bending_moment, t, ax)
                st.pyplot(fig)
            
            with col2:
                t_val_bending = st.slider(
                    "Select time for bending moment (s):",
                    min_value=float(t[0]),
                    max_value=float(t[-1]),
                    value=float(t[0])
                )
                fig, ax = plt.subplots()
                plot_bending_moment_by_time(t_val_bending, t, output_data['section_positions'], bending_moment, ax)
                st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred during calculation: {str(e)}")
        import traceback
        st.text(traceback.format_exc())

else:
    st.warning("Please upload a `.txt` file to begin calculations.")
