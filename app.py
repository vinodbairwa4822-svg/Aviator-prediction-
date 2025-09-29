import streamlit as st
import numpy as np
from typing import List

# --- 1. Constants ---
RISK_LIMIT_MAX = 6.00 
SAFE_FLOOR = 1.35 
USER_SIGNAL_THRESHOLD = 2.00 # आपका मास्टर सिग्नल पॉइंट

# --- 2. Helper Function: Flow Identification ---
def calculate_flow(multipliers: List[float]) -> str:
    """पिछले मल्टीप्लायर्स के आधार पर ट्रेंड (फ्लो) की पहचान करता है।"""
    if not multipliers or len(multipliers) < 6:
        return 'UNKNOWN'

    recent_6 = multipliers[-6:]
    avg_recent = np.mean(recent_6)
    
    # High-Value Multiplier Count (3.5x से ऊपर)
    high_value_count = sum(1 for x in recent_6 if x > 3.50)
    
    # Crash Count (1.50x से कम)
    crash_count = sum(1 for x in recent_6 if x < 1.50)

    if high_value_count >= 3:
        return 'LARGE_TREND_FLOW'
    elif crash_count >= 4:
        return 'SMALL_CRASH_FLOW'
    elif 2.00 <= avg_recent <= 3.50:
        return 'MEDIUM_MOMENTUM_FLOW'
    else:
        return 'SMALL_CRASH_FLOW'

# --- 3. Main Prediction Function ---
def predict_next_round_single(previous_multipliers: List[float]) -> str:
    
    if len(previous_multipliers) < 5:
        return "Smart Prediction: 1.50x (Need more data)"
    
    current_flow = calculate_flow(previous_multipliers)
    last_input = previous_multipliers[-1]

    # --- A. Master Control Rules ---

    # MASTER RULE A: 40x के बाद का अनिवार्य क्रैश रीसेट
    if last_input >= 40.0: 
        current_flow = 'FORCED_CRASH_RESET' 

    # MASTER RULE B: छोटे ट्रेंड को तोड़ने का आपका सिग्नल (> 2.0x)
    if current_flow == 'SMALL_CRASH_FLOW' and last_input > USER_SIGNAL_THRESHOLD:
        current_flow = 'MEDIUM_MOMENTUM_FLOW' 
    # MASTER RULE C: बड़े ट्रेंड को तोड़ने का लगातार 2 छोटे का सिग्नल
    elif current_flow == 'LARGE_TREND_FLOW' and sum(1 for x in previous_multipliers[-2:] if x < 1.50) >= 2:
        current_flow = 'SMALL_CRASH_FLOW' 

    # --- B. Base Calculation (Minimum Floor) ---
    last_5_avg = np.mean(previous_multipliers[-5:])
    # 1.35x का फ़्लोर लागू करें
    base_prediction = max(last_5_avg, SAFE_FLOOR) 
    
    smart_prediction = base_prediction

    # --- C. Smart Prediction Adjustment by Flow ---
    
    if current_flow == 'FORCED_CRASH_RESET':
        # 40x के बाद अनिवार्य रीसेट: 1.40x से ज़्यादा नहीं
        smart_prediction = min(1.40, base_prediction)
        
    elif current_flow == 'LARGE_TREND_FLOW':
        # मजबूत पैटर्न पर 4.5x तक सीमित
        smart_prediction = min(max(base_prediction * 1.5, 2.00), 4.50) 
        
    elif current_flow == 'MEDIUM_MOMENTUM_FLOW':
        # 1.80x से 3.5x के बीच
        smart_prediction = min(max(base_prediction * 1.3, 1.80), 3.50)
        
    elif current_flow == 'SMALL_CRASH_FLOW':
        # बिना सिग्नल के 2.0x से ज़्यादा नहीं
        smart_prediction = min(base_prediction * 1.1, 2.00)
        
        # बूस्ट लॉजिक (लगातार छोटे आने पर थोड़ा बढ़ाना)
        if sum(1 for x in previous_multipliers[-3:] if x < 1.35) >= 2:
            smart_prediction += 0.15

    # --- D. खराब पैटर्न पर चेतावनी (Streamlit) ---
    recent_4 = previous_multipliers[-4:]
    # खराब पैटर्न: 3-4 छोटे और फिर 1 बड़ा
    if sum(1 for x in recent_4 if x < 2.0) >= 3 and sum(1 for x in recent_4 if x > 3.0) >= 1:
        st.warning("⚠️ **Warning:** Trend is unstable (3-4 small followed by 1 big). Consider a safe cash-out.")


    # --- E. Final Output ---
    final_prediction = round(min(smart_prediction, RISK_LIMIT_MAX), 2)
    current_status = f"Flow: {current_flow.replace('_', ' ').title()}"
    
    return f"Smart Prediction: {final_prediction}x (Balanced Target). Status: {current_status}"

# --- Streamlit UI (आपको इसे अपनी UI में जोड़ना होगा) ---
# [यहां आपका Streamlit UI कोड आएगा, जो मल्टीप्लायर्स लेता है और 
# predict_next_round_single को कॉल करता है]

# उदाहरण के लिए, अगर आपके पास एक इनपुट लिस्ट है:
# input_list = st.text_input("Pichle Multipliers Daalein (Comma se alag karke)")
# if st.button("Analyze & Predict Next Round"):
#     try:
#         multipliers_float = [float(x.strip()) for x in input_list.split(',')]
#         if multipliers_float:
#             result = predict_next_round_single(multipliers_float)
#             st.success(result)
#     except Exception as e:
#         st.error(f"Input Error: Please check multiplier format. ({e})")
