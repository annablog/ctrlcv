# CircuitPython demo - Keyboard emulator

import time

import board
import digitalio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# A simple neat keyboard demo in CircuitPython

# The pins we'll use, each will have an internal pullup
keypress_pins = [board.D0, board.D3, board.D4]
# Our array of key objects
key_pin_array = []
# The Keycode sent for each button, will be paired with a control key
keys_pressed = [Keycode.CONTROL, Keycode.C, Keycode.V]

# The keyboard object!
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard()
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

# Make all pin objects inputs with pullups
for pin in keypress_pins:
    key_pin = digitalio.DigitalInOut(pin)
    key_pin.direction = digitalio.Direction.INPUT
    key_pin.pull = digitalio.Pull.UP
    key_pin_array.append(key_pin)

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

key_state_array = {}
for key in keys_pressed:
    key_state_array[key] = False

print("Waiting for key pin...")

while True:
    # Check each pin
    for key_pin in key_pin_array:
        i = key_pin_array.index(key_pin)
        key = keys_pressed[i] # Get the corresponding Keycode
        if not key_state_array[key] and not key_pin.value:  # Is it grounded?
            keyboard_layout.write("Pin %s has changed to grounded.\n" % key)
            # Turn on the red LED
            led.value = True
            key_state_array[key] = True


        if key_state_array[key] and key_pin.value:
            keyboard_layout.write("Pin %s has changed to not grounded.\n" % key)
        # "Type" the Keycode or string
            #keyboard.press(key)  # "Press"...
            #keyboard.release_all()  # ..."Release"!
            key_state_array[key] = False

        # Turn off the red LED
            led.value = False

    keys_to_press = []
    for key, value in key_state_array.items():
        if value:
            keys_to_press.append(key)
            keyboard_layout.write("Adding %s.\n" % key)
    if len(keys_to_press) > 0:
        keyboard_layout.write("Pressing %s.\n" % keys_to_press)
        # keyboard.press(keys_to_press)
        # keyboard.release_all()

    time.sleep(0.01)
