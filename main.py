# Code to control keyboard with 3 keys: CONTROL (D0), C (D3), V (D4)
# (i.e. the "Stack Overflow keyboard")

import time

import board
import digitalio
from adafruit_hid.keyboard import Keyboard
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

# Make all pin objects inputs with pullups
for pin in keypress_pins:
    key_pin = digitalio.DigitalInOut(pin)
    key_pin.direction = digitalio.Direction.INPUT
    key_pin.pull = digitalio.Pull.UP
    key_pin_array.append(key_pin)

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

key_state_array = {}
# Initialise all the keys as unpressed
for key in keys_pressed:
    key_state_array[key] = False

print("Waiting for key pin...")

while True:
    # Check each pin
    for key_pin in key_pin_array:
        i = key_pin_array.index(key_pin)
        key = keys_pressed[i]  # Get the corresponding Keycode
        if not key_state_array[key] and not key_pin.value:  # Is it grounded?
            # Register key as pressed
            key_state_array[key] = True

        if key_state_array[key] and key_pin.value:
            # Register key as unpressed
            key_state_array[key] = False

    # For each of the keys, if it's pressed, then actually press the key
    for key, value in key_state_array.items():
        if value:
            keyboard.press(key)

    # Release all keys
    keyboard.release_all()

    time.sleep(0.02)
