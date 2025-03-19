import board
import busio
import digitalio
import time

depth_trigger = digitalio.DigitalInOut(board.A1)
depth_trigger.direction = digitalio.Direction.OUTPUT
depth_trigger.value=False

import time
import board
from analogio import AnalogIn

analog_in = AnalogIn(board.A0)

uart = busio.UART(board.TX, board.RX, baudrate=115200, timeout=0)

def get_voltage(pin):
    return (pin.value * 3.3) / 65536


while True:
    
    voltage=get_voltage(analog_in)
    
    distance_mm=10240/3.3*voltage
    
    send_string=str(distance_mm)+" mm"
    
    print("Sending "+send_string)
    
    uart.write(bytes(send_string, "ascii"))

    time.sleep(10)
    

