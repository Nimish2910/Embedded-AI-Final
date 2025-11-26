import serial

ser = serial.Serial('/dev/serial0', 115200, timeout=1)

print("Listening...")

while True:
    line = ser.readline()
    if line:
        print(line.decode(errors='ignore').strip())
