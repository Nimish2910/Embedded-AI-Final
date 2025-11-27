import serial

ser = serial.Serial('/dev/serial0', 115200, timeout=1)

current_mode = "INT8"

print("Memory manager running...")

while True:
    line = ser.readline().decode(errors='ignore').strip()

    if line.startswith("MEM_FREE"):
        try:
            mem = int(line.split(":")[1].strip())

            # Simple adaptive logic
            if mem < 800:
                current_mode = "INT8"
            else:
                current_mode = "FP16"

            print(f"MODE SWITCH -> {current_mode}")

        except:
            pass

