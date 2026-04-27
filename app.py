from flask import Flask, request, jsonify
import joblib
import numpy as np

# Initialize app
app = Flask(__name__)

# Load model
model = joblib.load("model.pkl")

# ----------------------------
# Home Route
# ----------------------------
@app.route("/")
def home():
    return "API Running"

# ----------------------------
# Predict Route (Single + Bulk)
# ----------------------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        features = data["features"]

        # Convert to numpy array
        features = np.array(features)

        # Handle single input
        if features.ndim == 1:
            features = features.reshape(1, -1)

        # Predict
        predictions = model.predict(features)

        # If single input → return single prediction
        if len(predictions) == 1:
            return jsonify({
                "prediction": int(predictions[0])
            })

        # If bulk input → return list
        return jsonify({
            "predictions": predictions.tolist()
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })

# ----------------------------
# Run app (for local testing)
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
