import usb_cdc
from gamepad_state import GamepadState

data = usb_cdc.data

print(f"{usb_cdc.console=}")
print(f"{usb_cdc.data=}")
while True:
    if data.in_waiting:
        msg = data.readline()
        print("Received:", msg)  # goes to console REPL
        T1D_output = GamepadState.from_bytes(msg.strip())
        print(T1D_output)  # goes to console REPL
