import serial
import joblib
import numpy as np

# Load trained model
model = joblib.load("temp_model.pkl")

# Open serial port (same as working script)
ser = serial.Serial("/dev/serial0", 115200, timeout=1)

print("Listening to STM32...")

while True:
    try:
        line = ser.readline().decode("utf-8").strip()

        if not line:
            continue

        print("RAW:", line)   # Show what comes from STM32

        # Expect format: TEMP: 78
        if "TEMP" in line:
            parts = line.split(":")
            temp = float(parts[1].strip())

            # Prepare input for model
            X = np.array([[temp]])

            # Predict next value
            pred = model.predict(X)[0]

            print("Predicted next temp:", pred)

    except Exception as e:
        print("Error:", e)
