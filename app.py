import streamlit as st
import numpy as np
import joblib
import os

# Load model and scaler
model = joblib.load('xgb_fraud_model.pkl')
scaler = joblib.load('scaler.pkl')

st.title("💳 Credit Card Fraud Detector")
st.write("Enter transaction details to check if it's fraudulent.")

# Amount input
amount = st.number_input("Transaction Amount (€)", min_value=0.0, value=100.0)

# V1-V28 inputs
st.write("### PCA Features (V1 - V28)")
st.write("Default values represent a typical legitimate transaction.")

features = []
cols = st.columns(4)
for i in range(1, 29):
    col = cols[(i-1) % 4]
    val = col.number_input(f"V{i}", value=0.0, format="%.4f")
    features.append(val)

# Scale amount
amount_scaled = scaler.transform([[amount]])[0][0]

# Combine all features
input_data = np.array(features + [amount_scaled]).reshape(1, -1)

# Predict
if st.button("🔍 Predict"):
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    if prediction == 1:
        st.error(f"🚨 FRAUD DETECTED! Confidence: {probability*100:.1f}%")
    else:
        st.success(f"✅ Legitimate Transaction. Fraud Probability: {probability*100:.1f}%")