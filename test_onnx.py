import onnxruntime as ort
import numpy as np

session = ort.InferenceSession("temp_model.onnx")

input_name = session.get_inputs()[0].name

x = np.array([[80]], dtype=np.float32)

result = session.run(None, {input_name: x})

print("Prediction:", result)
