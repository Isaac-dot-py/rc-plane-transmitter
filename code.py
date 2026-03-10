import usb_cdc

data = usb_cdc.data

print(f"{usb_cdc.console=}")
print(f"{usb_cdc.data=}")
while True:
    if data.in_waiting:
        msg = data.readline()
        print("Received:", msg)  # goes to console REPL

        data.write(b"ack\n")