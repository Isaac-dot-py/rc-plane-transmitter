import usb_cdc
from gamepad_state import GamepadState
import pwmio
import board
from adafruit_motor import servo

# Use the data port (not REPL)
cdc = usb_cdc.data

# Initialize PWM output on GPIO 0-2 (GP0-2)
pwm1 = pwmio.PWMOut(board.GP0, duty_cycle=2**15, frequency=50)
servo1 = servo.Servo(pwm1)
pwm2 = pwmio.PWMOut(board.GP1, duty_cycle=2**15, frequency=50)
servo2 = servo.Servo(pwm2)
pwm3 = pwmio.PWMOut(board.GP2, duty_cycle=2**15, frequency=50)
servo3 = servo.Servo(pwm3)
pwm4 = pwmio.PWMOut(board.GP3, duty_cycle=2**15, frequency=50)
servo4 = servo.Servo(pwm4)

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
                angle1 = int(((state.RY + 1) / 2) * 180)
                servo1.angle = angle1
                angle2 = int(((state.RX + 1) / 2) * 180)
                servo2.angle = angle2
                angle3 = int(((state.LY + 1) / 2) * 180)
                servo3.angle = angle3
                angle4 = int(((state.LX + 1) / 2) * 180)
                servo4.angle = angle4
                print(
                    f"Right Y: {state.RY:.2f}, Angle: {angle1}, Right X: {state.RX:.2f}, Angle: {angle2}, Left Y: {state.LY:.2f}, Angle: {angle3}, Left X: {state.LX:.2f}, Angle: {angle4}",
                    end="\r",
                )
            else:
                print("Invalid state data: " + data_bytes.decode())
        except Exception as e:
            print(f"Error processing line: {e}")
    else:
        print("No data received")
