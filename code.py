import usb_cdc
from gamepad_state import GamepadState
import pwmio
import board
from adafruit_motor import servo

# Use the data port (not REPL)
cdc = usb_cdc.data

# Initialize PWM output on GPIO 0 (GP0)
pwm = pwmio.PWMOut(board.GP0, duty_cycle=2**15, frequency=50)
servo = servo.Servo(pwm)

while True:
    line = cdc.readline()
    if line:
        try:
            # Decode the hex string and convert it to bytes
            data_bytes = bytes.fromhex(line.decode().strip())
            # Create a GamepadState from the bytes
            state = GamepadState.from_bytes(data_bytes)
            if state:
                # Map right_y (-1 to 1) to angle (0 to 180)
                angle = int(((state.RY + 1) / 2) * 180)
                servo.angle = angle
                print(f"Right Y: {state.RY:.2f}, Angle: {angle}", end="\r")
            else:
                print("Invalid state data: " + data_bytes.decode())
        except Exception as e:
            print(f"Error processing line: {e}")
    else:
        print("No data received")
