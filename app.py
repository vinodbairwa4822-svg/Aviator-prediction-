import streamlit as st
import numpy as np
import pandas as pd
import random

# --- CONFIGURATION (Aapke Patterns ke Anusaar) ---
LOW_X_THRESHOLD = 1.80       # 1.80x se chhota = 'Chhota/Low'
MOMENTUM_BREAK_THRESHOLD = 2.00 # 2.00x se bada = 'Momentum Break/High-Medium'
SUPER_HIGH_THRESHOLD = 20.00 # 20x se bada = 'Super High/Extreme Risk'
LOOK_BACK_ROUNDS = 6         # Ab pichle 6 rounds dekhenge patterns ko behtar pehchanne ke liye

# --- STREAMLIT UI ---
st.title('Aviator Pattern Predictor (Final V8) 🎯')
st.caption("Yeh app aapke sabhi 'Down Flow Lock' aur 'Pattern Priority' rules par aadharit hai।")

# --- USER INPUT ---
last_multipliers_input = st.text_input(
    'Pichle Multipliers Daalein (Comma se alag karke)',
    # Example for testing Down Flow Lock: 4 bade, aur phir 5 chhote (Down Flow Active)
    '2.50, 3.10, 4.00, 2.10, 1.05, 1.20, 1.35, 1.60, 1.40' 
)

if st.button('Analyze & Predict Next Round'):
    try:
        multipliers = [float(x.strip()) for x in last_multipliers_input.split(',')]
        if len(multipliers) < LOOK_BACK_ROUNDS:
            st.error(f"Kripya kam se kam {LOOK_BACK_ROUNDS} multipliers daalein.")
            st.stop()
            
        df = pd.DataFrame({'Multiplier': multipliers})
        
        # --- PATTERN CHECKING AND COUNTING ---
        recent_rounds = multipliers[-LOOK_BACK_ROUNDS:]
        low_count_recent = sum(1 for x in recent_rounds if x < LOW_X_THRESHOLD)
        momentum_break_count = sum(1 for x in multipliers[-4:] if x >= MOMENTUM_BREAK_THRESHOLD)
        
        # DOWN FLOW LOCK LOGIC
        # Jab 3 ya 4 momentum break rounds aaye hain (2x+) aur latest round 2x se chhota hai, tab Down Flow Lock.
        down_flow_lock = (multipliers[-1] < MOMENTUM_BREAK_THRESHOLD) and (momentum_break_count >= 3)
        
        st.header("🔮 Next Round 'Guess' (Down Flow Lock Applied)")
        st.line_chart(df['Multiplier'])

        # --- PREDICTION LOGIC (Aapki Shartein Priority ke Saath) ---
        
        # 🔑 RULE 1: Super High X ke baad (Highest Risk)
        if any(x >= SUPER_HIGH_THRESHOLD for x in recent_rounds):
            prediction_guess = random.uniform(1.01, 1.25)
            st.error(f"🚨 **EXTREME LOW GUESS (HIGH RISK ZONE):** **{prediction_guess:.2f}x** (Super High X ke baad।)")
        
        # 🔑 RULE 2: Down Flow LOCK Active (Jab tak 2x+ nahi aaya, chota hi dega)
        elif down_flow_lock:
            prediction_guess = random.uniform(1.05, 1.70)
            st.warning(f"⬇️ **DOWN FLOW LOCK:** **{prediction_guess:.2f}x** (Lock Laga Hua Hai। Chote X aayenge।)")
            st.caption("💡 **Aapka Rule:** Jab tak aap khud 2x+ nahi daalenge, app 2x+ predict nahi karega।")
            
        # 🔑 RULE 3: VERY BEST Pattern (5-6 baar Bada Lagataar)
        # 4 ya 5 numbers 2x se bade aur 2 ya usse kam 1.80x se chote (momentum strong)
        elif sum(1 for x in multipliers[-6:] if x >= MOMENTUM_BREAK_THRESHOLD) >= 4 and low_count_recent <= 2:
            prediction_guess = random.uniform(3.5, 8.0)
            st.success(f"⭐⭐ **VERY BEST GUESS:** **{prediction_guess:.2f}x** (Strong Momentum। Jaisa aapne bataya, 4-5 bade lagataar!)")
            
        # 🔑 RULE 4: MEDIUM Pattern (2 Chote, 3 Bade, 1 Chota, 2 Bade - Zig Zag)
        # Yaani 6 rounds mein 3 ya 4 2x+ ke numbers ho, aur low count 2-3 ho
        elif 3 <= sum(1 for x in multipliers[-6:] if x >= MOMENTUM_BREAK_THRESHOLD) <= 4 and 2 <= low_count_recent <= 3:
            prediction_guess = random.uniform(2.0, 4.5)
            st.info(f"🔥 **MEDIUM GUESS:** **{prediction_guess:.2f}x** (Zig-Zag / Mixed Trend।)")

        # 🔑 RULE 5: KHARAB Pattern (3 Chote, 1 Bada)
        # Jab lagatar chote ki chain ban rahi ho, yaani 6 rounds mein 4 ya 5 low X
        elif low_count_recent >= 4 and sum(1 for x in multipliers[-6:] if x >= MOMENTUM_BREAK_THRESHOLD) <= 2:
            prediction_guess = random.uniform(1.85, 3.0)
            st.warning(f"📉 **KHARAB GUESS (BREAK CHANCE):** **{prediction_guess:.2f}x** (3-4 Chhote ke baad Bada aane ka chance।)")
            
        # 🔑 Default Low Risk (Koi pattern match nahi)
        else:
            prediction_guess = random.uniform(1.01, 1.70)
            st.error(f"📉 **Default LOW GUESS:** **{prediction_guess:.2f}x** (Clear pattern nahi। Risk kam lein।)")

    except ValueError:
        st.error("Kripya sahi format mein numbers daalein (Jaise: 1.50, 2.05)।")
    except Exception as e:
        st.error(f"Ek error hua: {e}")
