import streamlit as st
import requests
import pandas as pd

st.title("Malicious Log Detection System")

API_URL = "https://log-detection-ml-1.onrender.com/predict"

# ----------------------------
# SINGLE INPUT
# ----------------------------
st.header("Single Log Prediction")

ip = st.number_input("IP", 1, 255, 10)
status = st.selectbox("Status Code", [200, 404, 500])
requests_count = st.number_input("Requests", 1, 1000, 50)
bytes_ = st.number_input("Bytes", 100, 10000, 1000)

if st.button("Predict"):
    data = {
        "features": [ip, status, requests_count, bytes_]
    }
    response = requests.post(API_URL, json=data)

    result = response.json()
    if result["prediction"] == 1:
        st.error("⚠ Malicious Activity Detected")
    else:
        st.success("Normal Activity")

# ----------------------------
# FILE UPLOAD
# ----------------------------
st.header("Bulk Log Detection")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Input Data:", df)

    predictions = []
    for _, row in df.iterrows():
        data = {"features": row.tolist()}
        response = requests.post(API_URL, json=data)
        predictions.append(response.json()["prediction"])

    df["Prediction"] = predictions
    st.write("Output:", df)
