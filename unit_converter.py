import streamlit as st

# Set page configuration
st.set_page_config(page_title="Unit Converter", page_icon="⚖️", layout="centered")

# Custom CSS for advanced styling
st.markdown("""
    <style>
    /* Main Container Styling */
    .main-container {
        max-width: 600px;
        margin: auto;
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 0px 25px rgba(0, 0, 0, 0.3);
        font-family: 'Roboto', sans-serif;
    }

    /* Title Styling */
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #007BFF;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }

    /* Button Styling */
    .stButton>button {
        background-color:rgb(245, 237, 244);
        color: white;
        font-size: 18px;
        padding: 12px 24px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s, transform 0.2s;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
    }

    .stButton>button:hover {
        background-color:rgb(252, 167, 57);
        transform: scale(1.05);
    }

    .stButton>button:active {
        transform: scale(0.98);
    }

    /* Input Fields Styling */
    .stSelectbox, .stNumberInput {
        background-color:rgb(1, 7, 14);
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 10px;
        font-size: 16px;
        margin-top: 15px;
        box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);
    }

    .stSelectbox:focus, .stNumberInput:focus {
        border-color: #007BFF;
        box-shadow: 0 0 8px rgba(0, 123, 255, 0.6);
    }

    /* Result Container Styling */
    .result-container {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: #fff;
        background-color: rgba(0, 0, 0, 0.7);
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
    }

    /* History Section Styling */
    .history-container {
        margin-top: 30px;
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0px 0px 12px rgba(0, 0, 0, 0.2);
        font-size: 14px;
        font-family: 'Arial', sans-serif;
    }

    .history-container h3 {
        text-align: center;
        color: #333;
    }

    .history-container p {
        text-align: left;
        font-size: 16px;
        color: #555;
    }

    /* Reset Button Styling */
    .reset-button button {
        background-color: #dc3545;
        color: white;
        font-size: 18px;
        padding: 12px 24px;
        border-radius: 10px;
        cursor: pointer;
        transition: background-color 0.3s, transform 0.2s;
        border: none;
    }

    .reset-button button:hover {
        background-color: #c82333;
        transform: scale(1.05);
    }

    .reset-button button:active {
        transform: scale(0.98);
    }

    /* Footer Styling */
    .footer {
        text-align: center;
        color: #777;
        margin-top: 30px;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Conversion factors defined globally
conversion_factors = {
    "Length": {
        "Meter": 1, "Kilometer": 0.001, "Centimeter": 100, "Millimeter": 1000, "Mile": 0.000621371,
        "Yard": 1.09361, "Foot": 3.28084, "Inch": 39.3701
    },
    "Weight": {
        "Kilogram": 1, "Gram": 1000, "Milligram": 1e6, "Pound": 2.20462, "Ounce": 35.274, "Ton": 1e-3
    },
    "Temperature": {
        "Celsius": lambda x: x, "Fahrenheit": lambda x: (x * 9/5) + 32, "Kelvin": lambda x: x + 273.15
    },
    "Time": {
        "Second": 1, "Minute": 1/60, "Hour": 1/3600, "Day": 1/86400
    }
}

# Conversion logic
def convert_units(value, from_unit, to_unit, category):
    if category == "Temperature":
        if from_unit == "Celsius":
            return conversion_factors[category][to_unit](value)
        elif from_unit == "Fahrenheit":
            if to_unit == "Celsius":
                return (value - 32) * 5/9
            elif to_unit == "Kelvin":
                return (value - 32) * 5/9 + 273.15
        elif from_unit == "Kelvin":
            if to_unit == "Celsius":
                return value - 273.15
            elif to_unit == "Fahrenheit":
                return (value - 273.15) * 9/5 + 32
    else:
        return value * conversion_factors[category][to_unit] / conversion_factors[category][from_unit]

# Function to handle conversion history
if "history" not in st.session_state:
    st.session_state.history = []

def add_to_history(value, from_unit, to_unit, result, category):
    st.session_state.history.append(f"{value} {from_unit} = {result:.4f} {to_unit} ({category})")
    if len(st.session_state.history) > 5:
        st.session_state.history.pop(0)

# Reset function to clear session state and inputs
def reset_fields():
    st.session_state.history = []
    st.session_state["category"] = None
    st.session_state["from_unit"] = None
    st.session_state["to_unit"] = None
    st.session_state["value"] = None
    st.experimental_rerun()

# Main app layout
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<h1 class="title">🌟 Unit Converter</h1>', unsafe_allow_html=True)

# Select category
category = st.selectbox("Select Category", list(conversion_factors.keys()), key="category")

# Define units for selected category
units = list(conversion_factors[category].keys()) if category else []
from_unit = st.selectbox("From Unit", units, key="from_unit")
to_unit = st.selectbox("To Unit", units, key="to_unit")

# Input value
value = st.number_input("Enter Value", min_value=0.0, step=0.1, key="value")

# Conversion button
if st.button("Convert"):
    if value is not None and category and from_unit and to_unit:
        result = convert_units(value, from_unit, to_unit, category)
        if result is not None:
            st.markdown(f'<div class="result-container">Converted Value: {result:.4f} {to_unit}</div>', unsafe_allow_html=True)
            add_to_history(value, from_unit, to_unit, result, category)
        else:
            st.error("Conversion not supported!")
    else:
        st.error("Please complete all fields")

# Display history of conversions
if len(st.session_state.history) > 0:
    st.markdown('<div class="history-container"><h3>Conversion History</h3>', unsafe_allow_html=True)
    for record in st.session_state.history:
        st.markdown(f"<p>{record}</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Reset button to clear input fields and session state
if st.button("Reset", key="reset_button"):
    st.session_state.clear()

st.markdown("</div>", unsafe_allow_html=True)

# Footer Section
st.markdown('<div class="footer">Created by Saba Muhammad Riaz ❤️ using Streamlit</div>', unsafe_allow_html=True)






