import joblib
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

model = joblib.load("temp_model.pkl")

initial_type = [("float_input", FloatTensorType([None, 1]))]

onnx_model = convert_sklearn(model, initial_types=initial_type)

with open("temp_model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

print("ONNX model created")
