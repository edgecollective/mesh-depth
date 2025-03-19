import board
import busio
import digitalio
import time

depth_trigger = digitalio.DigitalInOut(board.A1)
depth_trigger.direction = digitalio.Direction.OUTPUT
depth_trigger.value=False

# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Analog In example"""
import time
import board
from analogio import AnalogIn

analog_in = AnalogIn(board.A0)


def get_voltage(pin):
    return (pin.value * 3.3) / 65536


while True:
    print((get_voltage(analog_in),))
    time.sleep(0.1)
