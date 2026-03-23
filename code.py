import usb_cdc
from gamepad_state import GamepadState
import pwmio
import board

# Use the data port (not REPL)
cdc = usb_cdc.data

# Initialize PWM output on GPIO 0 (GP0)
pwm = pwmio.PWMOut(board.GP0, frequency=1000, duty_cycle=0)

while True:
    line = cdc.readline()
    if line:
        try:
            # Decode the hex string and convert it to bytes
            data_bytes = bytes.fromhex(line.decode().strip())
            # Create a GamepadState from the bytes
            state = GamepadState.from_bytes(data_bytes)
            if state:
                # Map right_y (-1 to 1) to duty cycle (0 to 65535)
                duty = int(((state.RY + 1) / 2) * 65535)
                pwm.duty_cycle = duty
            else:
                print("Invalid state data: " + data_bytes.decode())
        except Exception as e:
            print(f"Error processing line: {e}")
    else:
        print("No data received")