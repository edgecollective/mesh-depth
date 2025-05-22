import board
import busio
import digitalio
import time

SLEEP_INTERVAL = 100


#uart_sense = busio.UART(board.A2, board.A3, baudrate=9600)

uart_mesh = busio.UART(board.TX, board.RX, baudrate=115200, timeout=0)

#while True:

    #depth="hello mesh!"
    
    #print("depth=",depth)
   
sendstring = "Evening, mesh!"

print("Sending "+sendstring)

uart_mesh.write(bytes(sendstring, "ascii"))

time.sleep(SLEEP_INTERVAL)

