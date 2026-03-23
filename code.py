import usb_cdc
from gamepad_state import GamepadState

# Use the data port (not REPL)
cdc = usb_cdc.data

while True:
    line = cdc.readline()
    if line:
        try:
            # Decode the hex string and convert it to bytes
            data_bytes = bytes.fromhex(line.decode().strip())
            # Create a GamepadState from the bytes
            state = GamepadState.from_bytes(data_bytes)
            print(state)
        except Exception as e:
            print(f"Error processing line: {e}")
    else:
        print("No data received")