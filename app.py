import streamlit as st
import numpy as np
import pandas as pd

st.title('Aviator Prediction App ✈️')
st.write("Yeh Streamlit app deployment test ke liye banaya gaya hai. Aap is code ko apni prediction logic se badal sakte hain.")

# User input lene ka option
last_multipliers = st.text_input(
    'Pichle Multipliers Daalein (Comma se alag karke)',
    '1.50, 2.05, 1.01, 3.10'
)

if st.button('Predict Next Round'):
    try:
        # Input ko process karna
        multipliers = [float(x.strip()) for x in last_multipliers.split(',')]
        
        # Ek dummy (nakli) prediction logic
        if len(multipliers) > 0 and multipliers[-1] < 1.50:
            prediction = np.random.uniform(1.8, 4.0)
            st.success(f"📈 Prediction: **{prediction:.2f}x** se upar ja sakta hai!")
        else:
            prediction = np.random.uniform(1.01, 1.5)
            st.warning(f"📉 Prediction: **{prediction:.2f}x** ke aas paas ruk sakta hai.")

    except ValueError:
        st.error("Kripya sahi format mein numbers daalein (Jaise: 1.50, 2.05).")

