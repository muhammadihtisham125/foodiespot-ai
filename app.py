import json
import pandas as pd
import streamlit as st
from google import genai

# Streamlit Page Configuration
st.set_page_config(
    page_title="FoodieSpot | Smart Range & Budget Finder",
    page_icon="🍔",
    layout="wide"
)

# --- CUSTOM CSS STYLING ---
st.markdown("""
<style>
    /* Main Background & Font */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 25px rgba(255, 107, 107, 0.3);
        margin-bottom: 25px;
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.95;
    }

    /* Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 18px;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    .metric-title {
        font-size: 0.9rem;
        color: #94a3b8;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: bold;
        color: #ff8e53;
    }

    /* Primary Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #ff6b6b 0%, #ff8e53 100%);
        color: white !important;
        font-weight: bold;
        border: none;
        padding: 12px 20px;
        border-radius: 12px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.6);
    }

    /* Section Cards */
    .content-card {
        background: rgba(30, 41, 59, 0.7);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- HERO BANNER ---
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🍕 FoodieSpot AI</div>
    <div class="hero-subtitle">Students & Travellers ke liye Smart Range, Budget & Food Finder 📍✨</div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR INPUTS ---
st.sidebar.markdown("### 📍 Search & Filters")
user_location = st.sidebar.text_input("🎯 Campus / Location:", value="Iqra University Islamabad")
max_distance = st.sidebar.slider("📏 Range Limit (km):", 0.5, 10.0, 3.0, step=0.5)
max_budget = st.sidebar.slider("💰 Max Budget (PKR):", 50, 2000, 500, step=50)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔑 API Setup")
api_key = st.sidebar.text_input("Gemini API Key:", type="password", help="Paste your Gemini API key here")

# --- AI DATA RETRIEVAL FUNCTION ---
def get_dynamic_food_spots(location, distance, budget, api_key):
    try:
        client = genai.Client(api_key=api_key)
        prompt = f"""
        Act as a local food guide for '{location}'. 
        Generate a JSON list of 5 realistic/popular food spots or restaurants near '{location}' 
        that fall within distance <= {distance} km and average price <= {budget} PKR.
        
        Return strictly ONLY a valid JSON array of objects with these exact keys:
        - "Restaurant / Spot"
        - "Cuisine"
        - "Avg Price (PKR)"
        - "Distance (km)"
        - "Best For"

        Do not include markdown code block formatting like ```json.
        """
        # Updated Model ID to gemini-3.8-flash
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:].strip()
        
        data = json.loads(text)
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"⚠️ Error fetching spots: {e}")
        return pd.DataFrame()

# --- METRIC DISPLAY DASHBOARD ---
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">📍 Current Location</div>
        <div class="metric-value">{user_location.split(',')[0]}</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">📏 Selected Range</div>
        <div class="metric-value">≤ {max_distance} km</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">💵 Budget Cap</div>
        <div class="metric-value">Rs. {max_budget}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- MAIN CONTROLE & DATA DISPLAY ---
st.markdown("### 🏬 Nearby Food Recommendations")

if not api_key:
    st.warning("🔑 Pehle sidebar mein apni **Gemini API Key** enter karein taake search start ho sake.")
else:
    if st.button("🔍 Find Nearby Food Spots Now"):
        with st.spinner("✨ Nearby best food spots search ho rahe hain..."):
            df_spots = get_dynamic_food_spots(user_location, max_distance, max_budget, api_key)
            st.session_state['df_spots'] = df_spots

    if 'df_spots' in st.session_state and not st.session_state['df_spots'].empty:
        st.dataframe(
            st.session_state['df_spots'],
            use_container_width=True,
            column_config={
                "Avg Price (PKR)": st.column_config.NumberColumn("Avg Price (PKR)", format="Rs. %d"),
                "Distance (km)": st.column_config.NumberColumn("Distance (km)", format="📍 %.1f km")
            }
        )
    elif 'df_spots' in st.session_state and st.session_state['df_spots'].empty:
        st.error("❌ Koi food spot nahi mila. Range ya budget badha kar try karein.")

st.markdown("---")

# --- AI ASSISTANT SECTION ---
st.markdown("### 🤖 Smart AI Food Concierge")

col_a, col_b = st.columns([3, 1])
with col_a:
    user_query = st.text_input("💬 Apni craving ya question likhein:", placeholder="e.g. High protein food under 300 PKR?")
with col_b:
    st.markdown("<br>", unsafe_allow_html=True)
    ask_ai = st.button("✨ Ask AI")

if ask_ai:
    if not api_key:
        st.error("⚠️ Sidebar mein API Key enter karein.")
    elif not user_query:
        st.info("💡 Pehle apna question type karein!")
    else:
        try:
            client = genai.Client(api_key=api_key)
            spots_info = st.session_state.get('df_spots', pd.DataFrame()).to_string(index=False) if 'df_spots' in st.session_state else "No data"
            
            context = f"User Location: {user_location}. Distance Limit: {max_distance} km. Budget: {max_budget} PKR.\nAvailable Spots Data:\n{spots_info}\n"
            prompt = f"{context}\nUser Question: {user_query}\nProvide a friendly, practical recommendation with emojis in simple English/Roman Urdu."

            with st.spinner("🤖 AI Recommendation tayyar kar raha hai..."):
                # Updated Model ID to gemini-3.8-flash
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                )
            
            st.markdown(f"""
            <div class="content-card">
                <h4>🎉 AI Recommendation:</h4>
                <p>{response.text}</p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {e}")

# --- COMPETITOR ANALYSIS ---
with st.expander("📊 Project Architecture & Competitor Insights"):
    st.markdown("""
    - **🚀 Fast Filtering:** Distance aur Budget slider ke saath direct hyper-local results.
    - **🤖 Generative Intelligence:** Gemini API ka use karke instant menu & dish advice.
    - **📱 Modern UX:** Dark theme, custom glassmorphism components aur clean layout.
    """)