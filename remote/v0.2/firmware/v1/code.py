import board
import busio
import digitalio
import time
from analogio import AnalogIn
import terminalio
import displayio

from adafruit_display_text import label
import adafruit_displayio_ssd1306

from adafruit_onewire.bus import OneWireBus

from adafruit_ds18x20 import DS18X20

# Initialize one-wire bus on board pin D5.
ow_bus = OneWireBus(board.D11)

# Scan for sensors and grab the first one found.
ds18 = DS18X20(ow_bus, ow_bus.scan()[0])

try:
    from i2cdisplaybus import I2CDisplayBus
except ImportError:
    from displayio import I2CDisplay as I2CDisplayBus
    
displayio.release_displays()
i2c = board.I2C()

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
display_bus = I2CDisplayBus(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# Make the display context
splash = displayio.Group()
display.root_group = splash


# Draw a label

text="startup..."

ta = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=5, y=5)
splash.append(ta)

ta.text="Water level via\n\nMeshtastic (TM)!"

time.sleep(2)

WAKEUP_TIME_SEC = 5 # if we're the one waking up the meshtastic node, change this to approx 6 sec or greater to give node time to wake up; if meshtastic node already powered, then this can be 0 or 1

# update: we might also set this to 10 just so that people get a reading on initial boot 

depth_trigger = digitalio.DigitalInOut(board.D10)
depth_trigger.direction = digitalio.Direction.OUTPUT
depth_trigger.value=False

done_pin = digitalio.DigitalInOut(board.D7)
done_pin.direction = digitalio.Direction.OUTPUT
done_pin.value=False

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value=False

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
    
done_pin.value=False

# sleep 5 seconds and show it
for i in range(0,WAKEUP_TIME_SEC):
    led.value=True
    time.sleep(1)
    led.value=False
    time.sleep(1)
    
# now the depth sensor should be powered

#depth=get_depth_crude()

battery = get_battery_voltage(analog_in)

#print("depth=",depth)

#ta.text="depth(mm): "+str(depth)+"\n\nbatt(V): "+str(battery)


temperature=f"{ds18.temperature:0.3f}"

ta.text="temp(C)="+temperature+"\n\nbatt(V):" + str(battery)

time.sleep(2)

sendstring = temperature+","+str(battery)

ta.text="Sending to mesh..."

print("Sending "+sendstring)

time.sleep(1)

uart_mesh.write(bytes(sendstring, "ascii"))

# 3 fast blinks, sent message to node
for i in range(0,3):
    led.value=True
    time.sleep(.1)
    led.value=False
    time.sleep(.1)
    


ta.text="Done! Sleeping..."

time.sleep(2)

# now pull DONE
done_pin.value=True

while True:
    led.value=True
    time.sleep(.2)
    led.value=False
    time.sleep(.2)
    led.value=True
    time.sleep(1)
    led.value=False
    time.sleep(.2)

#time.sleep(SLEEP_INTERVAL)

