import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load model directly
model = joblib.load("model.pkl")

st.set_page_config(page_title="Log Detection", layout="centered")
st.title("Malicious Log Detection System")

# ----------------------------
# SINGLE INPUT
# ----------------------------
st.header("Single Log Prediction")

ip = st.number_input("IP", 1, 255, 10)
status = st.selectbox("Status Code", [200, 404, 500])
requests_count = st.number_input("Requests", 1, 1000, 50)
bytes_ = st.number_input("Bytes", 100, 10000, 1000)

if st.button("Predict"):
    features = np.array([[ip, status, requests_count, bytes_]])
    prediction = model.predict(features)

    if prediction[0] == 1:
        st.error("⚠ Malicious Activity Detected")
    else:
        st.success("✅ Normal Activity")

# ----------------------------
# BULK INPUT
# ----------------------------
st.header("Bulk Log Detection")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Input Data:", df)

    predictions = model.predict(df.values)
    df["Prediction"] = predictions

    st.write("Output Data:", df)
