import onnxruntime as ort
import tracemalloc
import numpy as np

tracemalloc.start()
s = ort.InferenceSession('temp_model.onnx')
current, peak = tracemalloc.get_traced_memory()
print(f'Peak memory: {peak/1024:.2f} KB')


# Pre-allocate fixed input + output buffers
input_buf = np.zeros((1,1), dtype=np.float32)
output_buf = np.zeros((1,1), dtype=np.float32)

sess = ort.InferenceSession("temp_model.onnx")

print("Fixed memory region ready")
