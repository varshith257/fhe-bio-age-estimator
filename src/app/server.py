from flask import Flask, request, jsonify
from concrete.ml.deployment import FHEModelServer

app = Flask(__name__)
fhe_dir = "fhe_artifacts"
server = FHEModelServer(path_dir=fhe_dir)
server.load()

@app.route("/predict", methods=["POST"])
def predict():
    try:
        encrypted_data = request.json.get("data")
        serialized_evaluation_keys = request.json.get("keys")
        if not encrypted_data or not serialized_evaluation_keys:
            return jsonify({"error": "Missing encrypted data or keys"}), 400
        result = server.run(encrypted_data, serialized_evaluation_keys)
        return jsonify({"prediction": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
