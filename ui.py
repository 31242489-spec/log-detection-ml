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

    try:
        response = requests.post(API_URL, json=data)

        if response.status_code == 200:
            result = response.json()

            if "prediction" in result:
                if result["prediction"] == 1:
                    st.error("Malicious Activity")
                else:
                    st.success("Normal Activity")
            else:
                st.error("Invalid response from API")
                st.write(result)

        else:
            st.warning(f"API Error: {response.status_code}")

    except Exception as e:
        st.error(f"Request failed: {e}")


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
        # 🔹 Keep Name, but exclude for prediction
        features = df[["IP", "Status", "Requests", "Bytes"]]

        response = requests.post(API_URL, json={
            "features": features.values.tolist()
        })

        if response.status_code == 200:
            result = response.json()

            # 🔥 Handle both response types
            if "predictions" in result:
                predictions = result["predictions"]
            elif "prediction" in result:
                predictions = [result["prediction"]]
            else:
                st.error("Invalid API response")
                st.write(result)
                predictions = []

            if predictions:
                # Add prediction column
                df["Prediction"] = predictions

                # Convert to readable labels
                df["Prediction"] = df["Prediction"].apply(
                    lambda x: "Malicious" if x == 1 else "Normal"
                )

                st.subheader("Prediction Results")
                st.write(df)

        else:
            st.warning(f"API Error: {response.status_code}")
            st.write(response.text)

    except Exception as e:
        st.error(f"Error: {e}")
