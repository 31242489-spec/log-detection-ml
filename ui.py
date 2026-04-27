import streamlit as st
import requests
import pandas as pd

# 🔹 API URL
API_URL = "https://log-detection-ml-1.onrender.com/predict"

st.title("Malicious Log Detection System")

# =========================
# 🔹 SINGLE PREDICTION
# =========================
st.header("Single Log Prediction")

ip = st.number_input("IP", min_value=0)
status = st.selectbox("Status Code", [200, 404, 500])
requests_count = st.number_input("Requests", min_value=0)
bytes_data = st.number_input("Bytes", min_value=0)

if st.button("Predict"):
    data = {
        "features": [ip, status, requests_count, bytes_data]
    }

    response = requests.post(API_URL, json=data)

    if response.status_code == 200:
        result = response.json()

        if result["prediction"] == 1:
            st.error("Malicious Activity")
        else:
            st.success("Normal Activity")
    else:
        st.warning("API Error")


# =========================
# 🔹 BULK CSV UPLOAD
# =========================
st.header("Bulk Log Detection")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Data")
    st.write(df)

    try:
        # 🔹 Keep Name for display, but exclude from prediction
        features = df[["IP", "Status", "Requests", "Bytes"]]

        # 🔹 Send to API
        response = requests.post(API_URL, json={
            "features": features.values.tolist()
        })

        if response.status_code == 200:
            predictions = response.json()["predictions"]

            # 🔹 Add prediction column
            df["Prediction"] = predictions

            # 🔹 Convert to readable labels
            df["Prediction"] = df["Prediction"].apply(
                lambda x: "Malicious" if x == 1 else "Normal"
            )

            st.subheader("Prediction Results")
            st.write(df)

        else:
            st.warning("API Error")

    except Exception as e:
        st.error(f"Error: {e}")
