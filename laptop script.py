# WARNING DONT RUN ON PICO
import serial
import serial.tools.list_ports
import T1D_hack
import asyncio

for p in serial.tools.list_ports.comports():
    print(p.device, p.description, p.hwid)
portnum = input("Enter port number: ")
ser = serial.Serial(f"COM{portnum}", 115200)  # data port

def send_data_to_pico(data):
    ser.write(data)

async def main():
    # repeatedly read from the gamepad and send the bytes to the pico as hex strings, separated by newlines
    async for state in T1D_hack.gamepad_state_stream():
        if state is not None:
            send_data_to_pico(state.to_bytes().hex().encode())
            send_data_to_pico(b"\n")  # newline as a separator
            print(state.to_bytes().hex())


if __name__ == "__main__":
    asyncio.run(main())
