import joblib
import numpy as np

model = joblib.load("temp_model.pkl")

sample_temp = np.array([[79]])  # Your STM32 reading
pred = model.predict(sample_temp)

print("Predicted next temperature:", pred[0])
