import serial
import binascii

PORT = "/dev/serial0"   # change if your device name is different
BAUD = 115200           # agree this with STM32 teammate

ser = serial.Serial(PORT, BAUD, timeout=1)

print(f"Listening on {PORT} at {BAUD} baud... Press Ctrl+C to stop.")

try:
    while True:
        data = ser.read(32)   # read up to 32 bytes at a time
        if data:
            print("Got:", binascii.hexlify(data).decode())
except KeyboardInterrupt:
    print("Stopped.")
finally:
    ser.close()
