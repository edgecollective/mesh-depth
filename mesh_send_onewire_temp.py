import board
import busio
import digitalio
import time

SLEEP_INTERVAL = 100

from adafruit_onewire.bus import OneWireBus

from adafruit_ds18x20 import DS18X20

# Initialize one-wire bus on board pin D5.
ow_bus = OneWireBus(board.D11)

# Scan for sensors and grab the first one found.
ds18 = DS18X20(ow_bus, ow_bus.scan()[0])


uart_mesh = busio.UART(board.TX, board.RX, baudrate=115200, timeout=0)

sendstring = f"Temperature: {ds18.temperature:0.3f}C"

print("Sending "+sendstring)

uart_mesh.write(bytes(sendstring, "ascii"))

time.sleep(SLEEP_INTERVAL)

