# WARNING DONT RUN ON PICO
import serial
import serial.tools.list_ports

for p in serial.tools.list_ports.comports():
    print(p.device, p.description, p.hwid)
portnum = input("Enter port number: ")
ser = serial.Serial(f"COM{portnum}", 115200)  # data port
ser.write(b"hello\n")
print(ser.readline())
