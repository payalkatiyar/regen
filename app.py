import streamlit as st
import pandas as pd
import pickle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ReGen - Energy Prediction",
    page_icon="⚡",
    layout="wide"
)

# ---------------- DARK FUTURISTIC THEME ----------------
st.markdown("""
    <style>
        /* Global Layout */
        body {
            background: radial-gradient(circle at top left, #050d1a, #000000);
            color: #d4d8e0;
            font-family: 'Poppins', sans-serif;
        }

        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }

        /* Hero Section */
        .hero {
            text-align: center;
            padding: 4rem 2rem;
            border-radius: 2rem;
            background: linear-gradient(145deg, rgba(15,30,60,0.9), rgba(5,10,20,0.9));
            box-shadow: 0 0 50px rgba(50,100,255,0.15);
            backdrop-filter: blur(8px);
            margin-bottom: 2rem;
        }
        .hero h1 {
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, #50b7f5, #4c6ef5, #7c4df5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        .hero p {
            font-size: 1.2rem;
            color: #b0b7c3;
        }

        /* Input Card */
        .card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 1.5rem;
            padding: 2rem;
            box-shadow: 0 0 30px rgba(79, 110, 245, 0.15);
            transition: 0.3s;
            margin-bottom: 2rem;
        }
        .card:hover {
            box-shadow: 0 0 40px rgba(79, 110, 245, 0.3);
        }

        /* Headers */
        h2, h3 {
            color: #e6e9f0 !important;
        }

        /* Inputs */
        .stNumberInput input {
            background-color: rgba(255, 255, 255, 0.05) !important;
            color: #f0f4ff !important;
            border-radius: 0.5rem !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
        }

        /* Buttons */
        div.stButton > button:first-child {
            background: linear-gradient(90deg, #4c6ef5, #15aabf);
            color: white;
            border-radius: 0.75rem;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            border: none;
            transition: 0.3s;
        }
        div.stButton > button:first-child:hover {
            box-shadow: 0 0 20px rgba(76,110,245,0.5);
            transform: scale(1.03);
        }

        /* Result Box */
        .result-box {
            text-align: center;
            background: rgba(76, 110, 245, 0.08);
            border-radius: 1rem;
            padding: 1.5rem;
            margin-top: 1.5rem;
            box-shadow: 0 0 25px rgba(76, 110, 245, 0.25);
            border: 1px solid rgba(76,110,245,0.3);
        }
        .result-text {
            font-size: 1.6rem;
            color: #50b7f5;
            font-weight: 700;
        }

        /* Footer */
        footer {
            text-align: center;
            color: #7a8399;
            font-size: 0.9rem;
            margin-top: 3rem;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    try:
        with open("model.pkl", "rb") as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        st.error(f"⚠️ Model failed to load: {e}")
        return None

model = load_model()

# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="hero">
    <h1>⚡ ReGen</h1>
    <p>Predict Renewable Energy Output<br>— Smart • Clean • Sustainable —</p>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUT FORM (INSIDE CARD) ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🌤️ Environmental Inputs")

col1, col2 = st.columns(2)
with col1:
    temperature = st.number_input("🌡️ Temperature (°C)", value=25.0)
    humidity = st.number_input("💧 Humidity (%)", value=60.0)
    pressure = st.number_input("🎈 Pressure (hPa)", value=1013.0)
    precipitation = st.number_input("🌧️ Precipitation (mm)", value=0.0)
    cloud_cover = st.number_input("☁️ Cloud Cover (%)", value=40.0)

with col2:
    wind_speed_10 = st.number_input("🌬️ Wind Speed (10m, m/s)", value=5.0)
    wind_dir_10 = st.number_input("🧭 Wind Direction (°)", value=180.0)
    wind_speed_80 = st.number_input("🌪️ Wind Speed (80m, m/s)", value=7.0)
    shortwave_rad = st.number_input("🔆 Shortwave Radiation (W/m²)", value=200.0)
    angle_incidence = st.number_input("📐 Angle of Incidence (°)", value=30.0)

st.markdown("<br>", unsafe_allow_html=True)

# Centered Predict Button
st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
predict_clicked = st.button("🔮 Predict Energy Output")
st.markdown("</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)  # closes card

# ---------------- PREDICTION ----------------
if predict_clicked:
    if model is not None:
        input_data = pd.DataFrame([[
            temperature, humidity, pressure, precipitation, 0.0, cloud_cover,
            30.0, 20.0, 10.0, shortwave_rad, wind_speed_10, wind_dir_10,
            wind_speed_80, 200.0, 6.0, 250.0, 15.0, angle_incidence, 45.0, 120.0
        ]], columns=[
            'temperature_2_m_above_gnd', 'relative_humidity_2_m_above_gnd', 'mean_sea_level_pressure_MSL',
            'total_precipitation_sfc', 'snowfall_amount_sfc', 'total_cloud_cover_sfc',
            'high_cloud_cover_high_cld_lay', 'medium_cloud_cover_mid_cld_lay', 'low_cloud_cover_low_cld_lay',
            'shortwave_radiation_backwards_sfc', 'wind_speed_10_m_above_gnd', 'wind_direction_10_m_above_gnd',
            'wind_speed_80_m_above_gnd', 'wind_direction_80_m_above_gnd', 'wind_speed_900_mb',
            'wind_direction_900_mb', 'wind_gust_10_m_above_gnd', 'angle_of_incidence', 'zenith', 'azimuth'
        ])

        prediction = model.predict(input_data)[0]

        st.markdown(f"""
            <div class="result-box">
                <div class="result-text">⚡ Predicted Power Output: {prediction:.2f} kW</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Model not loaded. Please check your model.pkl file.")

# ---------------- FOOTER ----------------
st.markdown("""
<footer>
    Built by Charvi Sharma, Payal Katiyar, Rishika Raj and Rudranil Saha | SRM Institute of Science & Technology
</footer>
""", unsafe_allow_html=True)
