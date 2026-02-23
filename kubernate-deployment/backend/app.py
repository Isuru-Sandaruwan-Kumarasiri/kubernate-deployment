from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
import numpy as np

app = Flask(__name__)
CORS(app)

# 1. Load the model BEFORE running the app
model_path = os.path.join(os.path.dirname(__file__), "Training_models", "psb_lr_model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)

def logistic_regression_model(ph, ec, bd, pr, mc):
    new_data = np.array([[ph, ec, bd, pr, mc]])
    prediction = model.predict(new_data)
    return int(prediction[0])

# 2. Changed to POST to accept JSON body
@app.route('/classify', methods=['POST'])
def classify():
    try:
        data = request.json
        ph = float(data.get('ph'))
        ec = float(data.get('ec'))
        bd = float(data.get('bd'))
        pr = float(data.get('pr'))
        mc = float(data.get('mc'))

        result = logistic_regression_model(ph, ec, bd, pr, mc)
        
        # Ensure the key matches what the Frontend expects (prediction)
        return jsonify({'prediction': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    # Ensure port matches your fetch URL (5000)
    print("Server is starting...")
    app.run(host="0.0.0.0", port=5000, debug=True)