import streamlit as st
import numpy as np
import random
import matplotlib.pyplot as plt
from typing import List

# --- Constants ---
RISK_LIMIT_MAX = 6.00 
SAFE_FLOOR = 1.35 
USER_SIGNAL_THRESHOLD = 2.00

# --- Pattern Detection ---
def detect_pattern(multipliers: List[float]) -> str:
    if len(multipliers) < 4:
        return "INSUFFICIENT DATA"

    pattern = ["B" if m >= 2.0 else "C" for m in multipliers[-4:]]

    if pattern == ["B", "B", "C", "C"]:
        return "GOOD TREND"
    if pattern == ["B", "C", "C", "B"]:
        return "BAD TREND"
    if all(p == "C" for p in pattern[-3:]):
        return "SMALL TREND"

    return "UNKNOWN"

def check_trend_break(multipliers: List[float]) -> bool:
    if not multipliers:
        return False
    return multipliers[-1] >= 2.0

# --- Prediction Logic ---
def predict_next_round_single(previous_multipliers: List[float]) -> float:
    if len(previous_multipliers) < 5:
        return 1.50

    last_input = previous_multipliers[-1]
    last_5_avg = np.mean(previous_multipliers[-5:])
    base_prediction = max(last_5_avg, SAFE_FLOOR) 

    if detect_pattern(previous_multipliers) == "GOOD TREND":
        smart_prediction = min(base_prediction * 1.5, 4.50)
    elif detect_pattern(previous_multipliers) == "SMALL TREND":
        smart_prediction = min(base_prediction * 1.1, 2.00)
    elif detect_pattern(previous_multipliers) == "BAD TREND":
        smart_prediction = min(base_prediction * 1.2, 3.00)
    else:
        smart_prediction = base_prediction

    return round(min(smart_prediction, RISK_LIMIT_MAX), 2)

# --- Streamlit UI ---
st.set_page_config(page_title="Aviator Smart Prediction", layout="centered")
st.title("✈️ Aviator Prediction Analyst with Trend Detection 📊")

if "multipliers" not in st.session_state:
    st.session_state.multipliers = []

# Buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Generate Random Multiplier"):
        new_val = round(random.uniform(1.05, 6.00), 2)
        st.session_state.multipliers.append(new_val)
        if len(st.session_state.multipliers) > 30:
            st.session_state.multipliers.pop(0)
with col2:
    if st.button("Clear History"):
        st.session_state.multipliers = []
with col3:
    if st.button("Trend Analysis"):
        trend_status = detect_pattern(st.session_state.multipliers)
        st.info(f"Trend Status: {trend_status}")
        if check_trend_break(st.session_state.multipliers):
            st.success("📢 Trend break confirmed with ≥ 2× multiplier!")

# Input multipliers manually
input_list = st.text_area(
    "पिछले मल्टीप्लायर्स (कॉमा या नई लाइन से अलग):",
    value=", ".join(map(str, st.session_state.multipliers))
)

if st.button("Predict Next Round"):
    if not input_list:
        st.warning("कृपया मल्टीप्लायर्स इनपुट करें।")
    else:
        try:
            multipliers_str = input_list.replace('\n', ',')
            multipliers_float = [float(x.strip()) for x in multipliers_str.split(',') if x.strip()]
            
            if len(multipliers_float) < 5:
                st.error("कम से कम 5 मल्टीप्लायर्स ज़रूरी हैं।")
            else:
                prediction = predict_next_round_single(multipliers_float)
                trend_status = detect_pattern(multipliers_float)
                trend_break = check_trend_break(multipliers_float)

                st.success(f"🎯 Smart Prediction: {prediction}x")
                st.info(f"Trend Status: {trend_status}")
                if trend_break:
                    st.warning("📢 Trend break confirmed!")

                # Graph Plotting
                fig, ax = plt.subplots(figsize=(8,4))
                ax.plot(multipliers_float, marker='o', linestyle='-', color='blue', label="Multiplier History")
                ax.axhline(prediction, color='red', linestyle='--', label=f"Prediction: {prediction}x")
                ax.set_title("Aviator Multiplier Trend & Prediction")
                ax.set_xlabel("Rounds")
                ax.set_ylabel("Multiplier (x)")
                ax.legend()
                st.pyplot(fig)

        except ValueError:
            st.error("इनपुट में त्रुटि: सभी मान संख्याएँ (numbers) होने चाहिए।")
        except Exception as e:
            st.error(f"एक अप्रत्याशित त्रुटि आई: {e}")

# Show multiplier history
st.write("### 📊 Latest Multipliers History")
st.write(st.session_state.multipliers)
