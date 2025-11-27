import serial
import joblib
import numpy as np
import time

# --- UART setup ---
ser = serial.Serial('/dev/serial0', 115200, timeout=1)

# --- Load models ---
model_int8 = joblib.load("temp_model.pkl")
model_fp16 = joblib.load("temp_model.pkl")  # same file for now (acts as FP16)

# --- Default model ---
current_model = model_fp16
mode = "FP16"

print("Adaptive inference running...")

# --- Artificial memory pressure (to test switching) ---
memory_hog = []
try:
    for _ in range(50):  # 50MB total
        memory_hog.append(bytearray(1024 * 1024))  # 1MB each
except MemoryError:
    print("Memory allocation stopped (expected during test)")

# --- Main loop ---
while True:
    try:
        line = ser.readline().decode(errors='ignore').strip()

        # ---- Memory report handling ----
        if line.startswith("MEM_FREE"):
            try:
                mem = int(line.split(":")[1])

                # Switch based on memory
                if mem < 800:
                    current_model = model_int8
                    mode = "INT8"
                else:
                    current_model = model_fp16
                    mode = "FP16"

            except:
                pass

        # ---- Temperature handling ----
        if line.startswith("TEMP"):
            try:
                temp = int(line.split(":")[1])

                # ---- Measure inference latency ----
                input_data = np.array([[temp]])

                t0 = time.time()
                pred = current_model.predict(input_data)[0]
                t1 = time.time()

                latency_ms = (t1 - t0) * 1000

                # ---- Print results ----
                print(f"{mode} | RAW: {temp} | PRED: {pred:.2f} | LATENCY: {latency_ms:.2f} ms")

            except:
                pass

    except KeyboardInterrupt:
        print("Stopping...")
        break
