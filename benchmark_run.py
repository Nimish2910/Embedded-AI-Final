import serial
import time
import joblib
import numpy as np
import psutil

ser = serial.Serial('/dev/serial0', 115200, timeout=1)

model = joblib.load("temp_model.pkl")

log = open("benchmark_log.txt", "w")

print("Benchmark running...")

while True:
    line = ser.readline().decode(errors='ignore').strip()

    if line.startswith("TEMP"):
        try:
            temp = int(line.split(":")[1])

            mem_before = psutil.virtual_memory().used
            t0 = time.time()

            pred = model.predict(np.array([[temp]]))[0]

            t1 = time.time()
            mem_after = psutil.virtual_memory().used

            latency_ms = (t1 - t0) * 1000
            mem_kb = (mem_after - mem_before) / 1024

            log_line = f"{temp},{pred},{latency_ms:.2f},{mem_kb:.2f}\n"
            log.write(log_line)
            log.flush()

            print(log_line.strip())

        except:
            pass
