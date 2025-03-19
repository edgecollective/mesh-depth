import board
import busio
import digitalio
import time

depth_trigger = digitalio.DigitalInOut(board.A1)
depth_trigger.direction = digitalio.Direction.OUTPUT
depth_trigger.value=False


uart_sense = busio.UART(board.A2, board.A3, baudrate=9600)

uart_mesh = busio.UART(board.TX, board.RX, baudrate=115200, timeout=0)

def get_depth_crude():

    depth=-1
    
    data = uart_sense.read(32)  # read up to 32 bytes

    if data is not None:
       
        data_string = ''.join([chr(b) for b in data])
        #print("%r" % data_string)
        items = data_string.split('\r')
        for s in items:
            #print(s,len(s))
            if len(s)==5:
                depth=int(s[1:])
    return(depth)

while True:

    depth=get_depth_crude()
    
    print("depth=",depth)
   
    sendstring = str(depth)+ " mm"

    print("Sending "+sendstring)
    
    uart_mesh.write(bytes(sendstring, "ascii"))
    
    time.sleep(10)

