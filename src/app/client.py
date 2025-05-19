import gradio as gr
import requests
import numpy as np
from concrete.ml.deployment import FHEModelClient

client = FHEModelClient("fhe_artifacts", "client_keys")
client.get_serialized_evaluation_keys()

def predict_age(methylation_data):
    try:
        input_data = np.array([float(x.strip()) for x in methylation_data.split(",")]).reshape(1, -1)
        assert input_data.shape[1] == 5, "Expected exactly 5 CpG values."
        encrypted_data = client.quantize_encrypt_serialize(input_data)
        response = requests.post(
            "http://localhost:7860/predict",
            json={"data": encrypted_data, "keys": client.get_serialized_evaluation_keys()},
            timeout=60
        )
        if response.status_code != 200:
            return f"Server error: {response.text}"
        encrypted_result = response.json()["prediction"]
        result = client.deserialize_decrypt_dequantize(encrypted_result)
        return f"Predicted Biological Age: {result[0]:.2f} years"
    except Exception as e:
        return f"Error: {e}"

interface = gr.Interface(
    fn=predict_age,
    inputs=[gr.Number(label=f"cg{i+1}") for i in range(5)],
    # inputs=gr.Textbox(label="Enter 5 comma-separated methylation values (0–1)"),
    outputs=gr.Textbox(label="Predicted Biological Age"),
    examples=[[0.65, 0.23, 0.30, 0.42, 0.24]],
    title="🔒 Encrypted Biological Age Prediction",
    description="Enter methylation values for 5 CpG sites (0-1 range)"
)
interface.launch()
