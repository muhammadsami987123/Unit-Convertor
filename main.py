import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Pro Unit Converter",
    layout="centered"
)


st.markdown(
    """
    <style>
    /* Make the whole background a light gradient */
    body {
        background: linear-gradient(to bottom right, #f0f2f6, #ffffff);
        font-family: "Open Sans", sans-serif;
    }

    /* Center the main container and give it a max-width */
    .main .block-container {
        max-width: 800px;
        padding-top: 2rem;
        padding-bottom: 2rem;
        margin: auto;
    }

    /* Top banner (hero) style */
    .hero {
        background: #1e3c72; /* fallback for old browsers */
        background: linear-gradient(to right, #2a5298, #1e3c72);
        padding: 2rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
        text-align: center;
        color: #ffffff;
    }
    .hero h1 {
        margin: 0;
        font-size: 2rem;
    }
    .hero p {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    </style>
    """,
    unsafe_allow_html=True
)



LENGTH_UNITS_TO_METERS = {
    "Meter (m)": 1.0,
    "Centimeter (cm)": 0.01,
    "Kilometer (km)": 1000.0,
    "Inch (in)": 0.0254,
    "Foot (ft)": 0.3048
}

LENGTH_UNITS_FROM_METERS = {
    "Meter (m)": 1.0,
    "Centimeter (cm)": 100.0,
    "Kilometer (km)": 0.001,
    "Inch (in)": 39.3700787,
    "Foot (ft)": 3.2808399
}

def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    """Convert a length value from one unit to another, via meters."""
    if from_unit not in LENGTH_UNITS_TO_METERS or to_unit not in LENGTH_UNITS_FROM_METERS:
        raise ValueError("Unit not supported.")
   
    val_meters = value * LENGTH_UNITS_TO_METERS[from_unit]
   
    return val_meters * LENGTH_UNITS_FROM_METERS[to_unit]

def convert_length_to_all(value: float, from_unit: str) -> pd.DataFrame:
    """
    Convert a single 'value' in 'from_unit' to all other length units.
    Returns a DataFrame for a polished display.
    """
    rows = []
    for unit in LENGTH_UNITS_TO_METERS.keys():
        if unit != from_unit:  # skip the same unit if desired
            converted = convert_length(value, from_unit, unit)
            rows.append({"Target Unit": unit, "Converted Value": converted})
    df = pd.DataFrame(rows)
    return df



st.markdown(
    """
    <div class="hero">
      <h1>Pro Unit Converter</h1>
      <p>Convert length values among various units in a polished, modern interface.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write(
    "Select **Single Conversion** to convert from one unit to another, "
    "or **Multi Conversion** to see results in all available units."
)

tab_single, tab_multi = st.tabs(["Single Conversion", "Multi Conversion"])

# --- Single Conversion Tab ---
with tab_single:
    st.subheader("Single Conversion")
   
    with st.form(key="single_form"):
        col1, col2 = st.columns(2)
        with col1:
            from_unit = st.selectbox("From Unit", list(LENGTH_UNITS_TO_METERS.keys()), key="from_unit_single")
        with col2:
            to_unit = st.selectbox("To Unit", list(LENGTH_UNITS_TO_METERS.keys()), key="to_unit_single")

        value_single = st.number_input("Value:", min_value=0.0, format="%.4f", key="value_single")
        submitted_single = st.form_submit_button("Convert")

        if submitted_single:
            if from_unit == to_unit:
                st.info("From Unit and To Unit are the same. No conversion needed.")
            else:
                result_single = convert_length(value_single, from_unit, to_unit)
                st.success(f"{value_single} {from_unit} = {result_single:.4f} {to_unit}")


# --- Multi Conversion Tab ---
with tab_multi:
    st.subheader("Convert to All Units")
    
    with st.form(key="multi_form"):
        col1, _ = st.columns([2,1])  
        with col1:
            from_unit_multi = st.selectbox("From Unit", list(LENGTH_UNITS_TO_METERS.keys()), key="from_unit_multi")
            value_multi = st.number_input("Value:", min_value=0.0, format="%.4f", key="value_multi")

        submitted_multi = st.form_submit_button("Convert to All")

        if submitted_multi:
            df_result = convert_length_to_all(value_multi, from_unit_multi)
            st.success(f"Converted {value_multi} {from_unit_multi} to all other units:")
            # Display as a nicely formatted table
            st.dataframe(df_result.style.format({"Converted Value": "{:.4f}"}))


#  Footer 
st.markdown("---")  

st.markdown(
    """
    <div style="text-align: center; padding: 20px;">
        <p>Created by Muhammad Sami</p>
        <p>
            <a href="https://www.linkedin.com/in/muhammad-sami-3aa6102b8/" target="_blank" style="text-decoration: none; margin: 0 10px;">
                <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
            </a>
            <a href="https://github.com/muhammadsami987123" target="_blank" style="text-decoration: none; margin: 0 10px;">
                <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
            </a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

