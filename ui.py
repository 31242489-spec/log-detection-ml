import streamlit as st
import requests
import pandas as pd

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Log Detection System", layout="centered")

st.title("Malicious Log Detection System")

# ----------------------------
# API URL (IMPORTANT)
# ----------------------------
API_URL = "https://log-detection-ml-1.onrender.com/predict"

# ----------------------------
# SINGLE INPUT SECTION
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

    try:
        response = requests.post(
            API_URL,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        st.write("Status Code:", response.status_code)

        if response.status_code == 200:
            result = response.json()

            if result["prediction"] == 1:
                st.error("⚠ Malicious Activity Detected")
            else:
                st.success("✅ Normal Activity")
        else:
            st.error("API Error")
            st.write(response.text)

    except Exception as e:
        st.error(f"Request failed: {e}")

# ----------------------------
# BULK UPLOAD SECTION
# ----------------------------
st.header("Bulk Log Detection")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Input Data:", df)

    predictions = []

    for _, row in df.iterrows():
        data = {
            "features": row.tolist()
        }

        try:
            response = requests.post(
                API_URL,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                predictions.append(result.get("prediction", "error"))
            else:
                predictions.append("error")

        except:
            predictions.append("error")

    df["Prediction"] = predictions

    st.write("Output Data:", df)
