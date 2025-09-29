import streamlit as st # Streamlit का उपयोग चेतावनी (warning) दिखाने के लिए
import numpy as np # NumPy का उपयोग औसत (average) गणना के लिए

# --- Constants ---
RISK_LIMIT_MAX = 6.00 
SAFE_FLOOR = 1.35 
USER_SIGNAL_THRESHOLD = 2.00 # वह मान जिसके ऊपर आपका इनपुट ट्रेंड तोड़ता है

# --- Helper Function: Flow Identification ---
def calculate_flow(multipliers):
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

# --- Main Prediction Function ---
def predict_next_round_single(previous_multipliers):
    
    if len(previous_multipliers) < 5:
        # पर्याप्त डेटा न होने पर डिफ़ॉल्ट मान
        return "Smart Prediction: 1.50x (Need more data)"
    
    current_flow = calculate_flow(previous_multipliers)
    last_input = previous_multipliers[-1]

    # --- 1. Master Control Rules ---

    # MASTER RULE A: 50x के बाद का अनिवार्य क्रैश रीसेट
    if last_input >= 40.0: 
        current_flow = 'FORCED_CRASH_RESET' 

    # MASTER RULE B: छोटे ट्रेंड को तोड़ने का आपका सिग्नल (> 2.0x)
    # यह नियम बिना आपके सिग्नल के बड़े नंबर देने से रोकता है।
    if current_flow == 'SMALL_CRASH_FLOW' and last_input > USER_SIGNAL_THRESHOLD:
        current_flow = 'MEDIUM_MOMENTUM_FLOW' # ट्रेंड ब्रेक!
    elif current_flow == 'LARGE_TREND_FLOW' and sum(1 for x in previous_multipliers[-2:] if x < 1.50) >= 2:
        current_flow = 'SMALL_CRASH_FLOW' # लगातार 2 छोटे आने पर ट्रेंड ब्रेक!

    # --- 2. Base Calculation ---
    last_5_avg = np.mean(previous_multipliers[-5:])
    # 1.35x का फ़्लोर लागू करें (Minimum Prediction इतना ज़रूर रहेगा)
    base_prediction = max(last_5_avg, SAFE_FLOOR) 
    
    smart_prediction = base_prediction

    # --- 3. Smart Prediction Adjustment by Flow ---
    
    if current_flow == 'FORCED_CRASH_RESET':
        # 50x के बाद का रीसेट: 1.40x से ज़्यादा नहीं
        smart_prediction = min(1.40, base_prediction)
        
    elif current_flow == 'LARGE_TREND_FLOW':
        # 4 बड़े 1 छोटा जैसे मजबूत पैटर्न पर 4.5x तक सीमित
        # Min को 2.0x पर पुश करें
        smart_prediction = min(max(base_prediction * 1.5, 2.00), 4.50) 
        
    elif current_flow == 'MEDIUM_MOMENTUM_FLOW':
        # 1 बड़ा 1 छोटा जैसे पैटर्न में 3.5x तक सीमित
        # Min को 1.80x पर पुश करें
        smart_prediction = min(max(base_prediction * 1.3, 1.80), 3.50)
        
    elif current_flow == 'SMALL_CRASH_FLOW':
        # बिना सिग्नल के 2.0x से ज़्यादा नहीं
        smart_prediction = min(base_prediction * 1.1, 2.00)
        
        # (बूस्ट लॉजिक: अगर 2 बार 1.35x से कम आया, तो 0.15x का बूस्ट दें)
        if sum(1 for x in previous_multipliers[-3:] if x < 1.35) >= 2:
            smart_prediction += 0.15

    # --- 4. खराब पैटर्न पर चेतावनी (Warning on Bad Patterns) ---
    recent_4 = previous_multipliers[-4:]
    # खराब पैटर्न: 3-4 छोटे followed by 1 बड़ा (3 बार छोटे और 1 बार बड़ा)
    if sum(1 for x in recent_4 if x < 2.0) >= 3 and sum(1 for x in recent_4 if x > 3.0) >= 1:
        st.warning("⚠️ **Warning:** Trend is unstable (3-4 small followed by 1 big). Consider a safe cash-out.")


    # --- 5. Final Output ---
    
    # 2 दशमलव स्थानों तक सीमित करें
    final_prediction = round(min(smart_prediction, RISK_LIMIT_MAX), 2) # 6.0x से ऊपर नहीं जाएगा

    return f"Smart Prediction: {final_prediction}x (Balanced Target)"
