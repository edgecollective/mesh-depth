import board
import busio
import digitalio
import time
from analogio import AnalogIn

SLEEP_INTERVAL = 600 # very 10 minutes

depth_trigger = digitalio.DigitalInOut(board.D10)
depth_trigger.direction = digitalio.Direction.OUTPUT
depth_trigger.value=False

done_pin = digitalio.DigitalInOut(board.D7)
done_pin.direction = digitalio.Direction.OUTPUT
done_pin.value=False

analog_in = AnalogIn(board.A4)

uart_sense = busio.UART(board.A2, board.A3, baudrate=9600)

uart_mesh = busio.UART(board.TX, board.RX, baudrate=115200, timeout=0)

def get_depth_crude():

    depth=-1
    
    depth_trigger.value=True
    time.sleep(.1)
    data = uart_sense.reset_input_buffer()
    data = uart_sense.read(32)  # read up to 32 bytes

    if data is not None:
       
        data_string = ''.join([chr(b) for b in data])
        #print("%r" % data_string)
        items = data_string.split('\r')
        for s in items:
            #print(s,len(s))
            if len(s)==5:
                depth=int(s[1:])
                
    depth_trigger.value=False
    return(depth)

def get_battery_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2 # even voltage divider
    
while True:

    depth=get_depth_crude()
    battery = get_battery_voltage(analog_in)
    
    print("depth=",depth)
   
    sendstring = str(depth)+","+str(battery)

    print("Sending "+sendstring)
    
    uart_mesh.write(bytes(sendstring, "ascii"))
    
    time.sleep(SLEEP_INTERVAL)

