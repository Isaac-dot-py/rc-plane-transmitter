import board
import digitalio
import adafruit_rfm69
import usb.core
import usb_host
import busio
import adafruit_usb_host_descriptors
import gamepad_state
from time import sleep

CLOCK_PIN = board.GP2
MISO_PIN = board.GP4
MOSI_PIN = board.GP3
CS_PIN = board.GP5
RESET_PIN = board.GP6
RADIO_FREQ_MHZ = 915.0

usb_host.Port(board.GP1, board.GP0)

# Define Chip Select and Reset pins for the radio module.
radio_cs = digitalio.DigitalInOut(CS_PIN)
radio_reset = digitalio.DigitalInOut(RESET_PIN)
radio_spi = busio.SPI(clock=CLOCK_PIN, MOSI=MOSI_PIN, MISO=MISO_PIN)

# Initialise RFM69 radio
rfm69 = adafruit_rfm69.RFM69(radio_spi, radio_cs, radio_reset, RADIO_FREQ_MHZ)


joystick_device = None
joystick_endpoint = None
report_length = 64  # generous buffer; trimmed after we see real reports

print("Waiting for USB device...")

while joystick_device is None:
    for device in usb.core.find(find_all=True):
        interface_index, endpoint_address = (
            adafruit_usb_host_descriptors.find_joystick_endpoint(device)
        )
        if endpoint_address is not None:
            joystick_device = device
            joystick_endpoint = endpoint_address
            print(f"Found joystick: {device.idVendor:04x}:{device.idProduct:04x}")
            print(f"  interface {interface_index}, endpoint {hex(endpoint_address)}")
            break
    sleep(0.1)

# Detach any kernel/CircuitPython-internal driver and claim the interface
try:
    joystick_device.set_configuration()
    if joystick_device.is_kernel_driver_active(interface_index):
        joystick_device.detach_kernel_driver(interface_index)
except usb.core.USBError:
    print("usberror")

buf = bytearray(report_length)
last = None

# Byte offsets for a Logitech Extreme 3D Pro's 7-byte HID report.
# If your raw hex dump doesn't line up with this (e.g. everything shifted
# by one byte), your transport is prepending a Report ID byte -- adjust
# OFFSET below to 1 and re-check.
OFFSET = 0

HAT_TO_DEGREES = (0, 45, 90, 135, 180, 225, 270, 315, -1)  # 8=centered -> -1


def parse_report(data):
    d = data[OFFSET:]
    if len(d) < 7:
        return None

    x = d[0] | ((d[1] & 0x03) << 8)  # 0..1023
    y = (d[1] >> 2) | ((d[2] & 0x0F) << 6)  # 0..1023
    hat_nibble = d[2] >> 4  # 0..8 (8 = centered)
    twist = d[3]  # 0..255
    buttons_a = d[4]
    slider = d[5]  # 0..255
    buttons_b = d[6]

    axes = [x, y, twist, slider]  # index 0=X, 1=Y, 2=twist(Z), 3=slider/throttle

    buttons_mask = buttons_a | (buttons_b << 8)
    buttons = [bool(buttons_mask & (1 << i)) for i in range(12)]  # 12 buttons

    pov = HAT_TO_DEGREES[hat_nibble] if hat_nibble < len(HAT_TO_DEGREES) else -1

    return axes, buttons, pov


print("Reading reports -- move sticks / press buttons to see which bytes change.")

while True:
    try:
        count = joystick_device.read(joystick_endpoint, buf, timeout=50)
        print("test")
        data = bytes(buf[:count])
        if data != last:
            print(" ".join(f"{b:02x}" for b in data))
            parsed = parse_report(data)
            if parsed:
                axes, buttons, pov = parsed
                print("axes:", axes, "buttons:", buttons, "pov:", pov)
            last = data
    except usb.core.USBTimeoutError:
        print("USB timeout (no data received)")
    except usb.core.USBError as e:
        print("USB error (device unplugged?):", e)
        sleep(1)
    # try:
    #     data = bytes.fromhex("01 02 03 04 05 06 07 08")  # Example data to send
    #     rfm69.send(data)
    #     print(f"Sent data: {data.hex()}", end="\r")
    # except Exception as e:
    #     print(f"Error sending data: {e}")
