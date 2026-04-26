from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("model.pkl")

# ----------------------------
# CORS FIX (IMPORTANT)
# ----------------------------
@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    return response

# ----------------------------
# HOME
# ----------------------------
@app.route("/")
def home():
    return "API Running"

# ----------------------------
# PREDICT
# ----------------------------
@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"})  # preflight response

    try:
        data = request.get_json(force=True)
        features = np.array(data["features"]).reshape(1, -1)

        prediction = model.predict(features)

        return jsonify({"prediction": int(prediction[0])})

    except Exception as e:
        return jsonify({"error": str(e)})
