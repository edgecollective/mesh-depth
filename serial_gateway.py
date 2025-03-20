import board
import busio
import digitalio
import time


uart_mesh = busio.UART(board.TX, board.RX, baudrate=115200, timeout=0)


while True:

    data = uart_mesh.read(32)
    
    if data is not None:
       
        data_string = ''.join([chr(b) for b in data])
        #print("%r" % data_string)
        #print(data_string)
        items = data_string.split(":")
        #print(items)
        if len(items)==2:
            depth=items[1].strip()
            print(depth)
            

        

