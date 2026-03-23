import asyncio
import bleak
import vgamepad
from vgamepad import XUSB_BUTTON
from gamepad_state import *

MAC_ADDRESS = "C6:86:A1:06:8B:7C"
CHAR_UUID = "00008651-0000-1000-8000-00805f9b34fb"
button_map = {
    "L1": "XUSB_GAMEPAD_LEFT_SHOULDER",
    "R1": "XUSB_GAMEPAD_RIGHT_SHOULDER",
    "X": "XUSB_GAMEPAD_X",
    "Y": "XUSB_GAMEPAD_Y",
    "A": "XUSB_GAMEPAD_A",
    "B": "XUSB_GAMEPAD_B",
    "C1": "XUSB_GAMEPAD_BACK",
    "C2": "XUSB_GAMEPAD_START",
    "MENU": "XUSB_GAMEPAD_GUIDE",
    "down": "XUSB_GAMEPAD_DPAD_DOWN",
    "up": "XUSB_GAMEPAD_DPAD_UP",
    "left": "XUSB_GAMEPAD_DPAD_LEFT",
    "right": "XUSB_GAMEPAD_DPAD_RIGHT",
}


async def gamepad_state_stream(
    mac_address: str = MAC_ADDRESS,
    char_uuid: str = CHAR_UUID,
):
    while True:
        try:
            async with bleak.BleakClient(mac_address) as t1d:
                while True:
                    raw = await t1d.read_gatt_char(char_uuid)
                    state = parse_state(raw)
                    if state is None:
                        yield None
                    yield state
        except OSError:
            print("bluetooth not on")
            yield None
        except KeyboardInterrupt:
            print("Exiting on Ctrl+C")
            break


async def run_vgamepad(
    mac_address: str = MAC_ADDRESS,
    char_uuid: str = CHAR_UUID,
) -> None:
    prev_states = dict.fromkeys(button_map, False)
    gamepad = vgamepad.VX360Gamepad()

    async for state in gamepad_state_stream(mac_address, char_uuid):
        if state is None:
            gamepad.update()
            continue
        for button, gamepad_button in button_map.items():
            current_state = getattr(state, button)
            if current_state and not prev_states[button]:
                gamepad.press_button(button=getattr(XUSB_BUTTON, gamepad_button))
            elif not current_state and prev_states[button]:
                gamepad.release_button(button=getattr(XUSB_BUTTON, gamepad_button))

        gamepad.left_trigger(value=state.L2)
        gamepad.right_trigger(value=state.R2)
        gamepad.left_joystick_float(state.LX, state.LY)
        gamepad.right_joystick_float(state.RX, state.RY)
        gamepad.update()

        for button in button_map:
            prev_states[button] = getattr(state, button)


async def main() -> None:
    await run_vgamepad()


if __name__ == "__main__":
    asyncio.run(main())
