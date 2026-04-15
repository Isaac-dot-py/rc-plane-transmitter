# import usb_cdc
# from gamepad_state import GamepadState
# import pwmio
# import board
# from adafruit_motor import servo

# MIN_THROTTLE = 58
# MAX_THROTTLE = 180

# # Use the data port (not REPL)
# cdc = usb_cdc.data

# # Initialize PWM output on GPIO 0-2 (GP0-2)
# pwm1 = pwmio.PWMOut(board.GP0, duty_cycle=2**15, frequency=50)
# servo1 = servo.Servo(pwm1)
# pwm2 = pwmio.PWMOut(board.GP1, duty_cycle=2**15, frequency=50)
# servo2 = servo.Servo(pwm2)
# throttle_pwm = pwmio.PWMOut(board.GP2, duty_cycle=2**15, frequency=50)
# throttle_servo = servo.Servo(throttle_pwm)
# pwm4 = pwmio.PWMOut(board.GP3, duty_cycle=2**15, frequency=50)
# servo4 = servo.Servo(pwm4)

# armed = False

# while True:
#     line = cdc.readline()
#     if line:
#         try:
#             # Decode the hex string and convert it to bytes
#             data_bytes = bytes.fromhex(line.decode().strip())
#             # Create a GamepadState from the bytes
#             state = GamepadState.from_bytes(data_bytes)
#             if state:
#                 # C2 is arming button, arm when C2 is pressed and throttle is at minimum
#                 if state.C2 and not armed and state.LY < -0.95:
#                     armed = True
#                 # Disarm when C1 is pressed
#                 if state.C1 and armed:
#                     armed = False

#                 # Map input (-1 to 1) to angle (0 to 180)
#                 angle1 = int(((state.RY + 1) / 2) * 180)
#                 servo1.angle = angle1
#                 angle2 = int(((state.RX + 1) / 2) * 180)
#                 servo2.angle = angle2
#                 angle4 = int(((state.LX + 1) / 2) * 180)
#                 servo4.angle = angle4

#                 throttle_angle = (
#                     int(
#                         ((state.LY + 1) / 2) * (MAX_THROTTLE - MIN_THROTTLE)
#                         + MIN_THROTTLE
#                     )
#                     if armed
#                     else 20
#                 )
#                 throttle_servo.angle = throttle_angle
#                 print(
#                     f"Right Y: {round(state.RY, 2):<5}, Angle: {angle1:<3}, Right X: {round(state.RX, 2):<5}, Angle: {angle2:<3}, Left Y: {round(state.LY, 2):<5}, Throttle Angle: {throttle_angle:<3}, Left X: {round(state.LX, 2):<5}, Angle: {angle4:<3}",
#                     end="\r",
#                 )
#             else:
#                 print("Invalid state data: " + data_bytes.decode())
#         except Exception as e:
#             print(f"Error processing line: {e}")
#     else:
#         print("No data received")


import board



CS_PIN = board.GP0
RESET_PIN = board.GP1
CLOCK_PIN = board.GP2
MOSI_PIN = board.GP3
MISO_PIN = board.GP4



import digitalio
import adafruit_rfm69
import busio
from time import sleep

# Define radio frequency in MHz. Must match your
# module. Can be a value like 915.0, 433.0, etc.
RADIO_FREQ_MHZ = 915.0

# Define Chip Select and Reset pins for the radio module.
CS = digitalio.DigitalInOut(CS_PIN)
RESET = digitalio.DigitalInOut(RESET_PIN)
spi = busio.SPI(clock=CLOCK_PIN, MOSI=MOSI_PIN, MISO=MISO_PIN)

# Initialise RFM69 radio
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ)

while True:
    rfm69.send(bytes("button", "UTF-8"))
    input("Sent 'button' packet. Press Enter to send again...")