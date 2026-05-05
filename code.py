TRANSMIT_RANDOM_GAMEPAD_STATE = False

import usb_cdc
import board
import digitalio
import adafruit_rfm69
import busio
import gamepad_state


CS_PIN = board.GP0
RESET_PIN = board.GP1
CLOCK_PIN = board.GP2
MOSI_PIN = board.GP3
MISO_PIN = board.GP4
RADIO_FREQ_MHZ = 915.0


# Use the data port (not REPL)
cdc = usb_cdc.data

# Define Chip Select and Reset pins for the radio module.
radio_cs = digitalio.DigitalInOut(CS_PIN)
radio_reset = digitalio.DigitalInOut(RESET_PIN)
radio_spi = busio.SPI(clock=CLOCK_PIN, MOSI=MOSI_PIN, MISO=MISO_PIN)

# Initialise RFM69 radio
rfm69 = adafruit_rfm69.RFM69(radio_spi, radio_cs, radio_reset, RADIO_FREQ_MHZ)

   
while True:
    if TRANSMIT_RANDOM_GAMEPAD_STATE:
        random_state = gamepad_state.random_state()
        try:
            rfm69.send(random_state.to_bytes().hex().encode())
        except Exception as e:
            print(f"Error sending random state: {e}")
        continue
    try:
        line = cdc.readline()
        if line:
            try:
                # Decode the hex string and convert it to bytes
                gamepadstate_in_bytes = bytes.fromhex(line.decode().strip())
                try:
                    rfm69.send(gamepadstate_in_bytes)
                except Exception as e:
                    print(f"Error sending data: {e}")
            except Exception as e:
                print(f"Error processing line: {line} {e}")
        else:
            print("No data received")
    except Exception as e:
        print(f"Error reading from data COM port: {e}")
